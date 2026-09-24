"""Conservative fixed-element candidate detection for real architectural artifacts.

This module detects evidence-backed *candidates* but never promotes uncertain
visual candidates to LOCKED. Approval-grade locking remains fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import cv2
import fitz
import numpy as np


_PLAN_TITLE_RE = re.compile(r"\bPLANTA\s+([^\n]+)", re.I)
_FIXED_TYPES = (
    "COLUMNS",
    "OUTER_BOUNDARY",
    "WALLS",
    "DOORS",
    "WINDOWS",
    "OVERALL_PLAN_FORM",
)


@dataclass(frozen=True)
class LockedElementCandidate:
    candidate_id: str
    element_type: str
    bbox: tuple[float, float, float, float]
    confidence: float
    evidence_ids: tuple[str, ...]
    status: str
    rationale: str

    def validate(self) -> None:
        if not self.candidate_id or self.element_type not in _FIXED_TYPES:
            raise ValueError("INVALID_LOCKED_ELEMENT_CANDIDATE")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("INVALID_CANDIDATE_CONFIDENCE")
        if not self.evidence_ids:
            raise ValueError("MISSING_CANDIDATE_EVIDENCE")
        if self.status == "LOCKED" and self.confidence < 0.95:
            raise ValueError("LOCKED_CANDIDATE_CONFIDENCE_TOO_LOW")


class ConservativeLockedElementDetector:
    """Extract plan-level vector evidence and structural candidates without guessing."""

    detector_id = "conservative-vector-fixed-v0.2"

    def detect(self, source_path: str, source_sha256: str) -> dict[str, Any]:
        path = Path(source_path)
        if path.suffix.lower() != ".pdf":
            return self._raster_fallback(source_sha256)

        document = fitz.open(path)
        if document.page_count == 0:
            return {
                "status": "UNKNOWN",
                "reason": "SOURCE_DOCUMENT_EMPTY",
                "plan_panels": [],
                "candidates": [],
            }

        page = document[0]
        blocks = page.get_text("blocks")
        titles = []
        for block_index, block in enumerate(blocks):
            text = block[4].strip()
            matches = list(_PLAN_TITLE_RE.finditer(text))
            for match_index, match in enumerate(matches):
                title = f"PLANTA {match.group(1).strip()}"
                titles.append({
                    "index": len(titles) + 1,
                    "title": title,
                    "bbox": [float(block[0]), float(block[1]), float(block[2]), float(block[3])],
                    "evidence_id": f"pdf-text-block-{block_index}-{match_index}",
                })

        drawings = page.get_drawings()
        vertical_lines = []
        filled_rects = []
        horizontal_lines = []
        for drawing_index, drawing in enumerate(drawings):
            rect = drawing.get("rect")
            if rect is not None and drawing.get("fill") is not None:
                w, h = rect.width, rect.height
                if 20 <= w <= 80 and 20 <= h <= 80:
                    filled_rects.append((drawing_index, rect))
            for item in drawing.get("items", []):
                if item and item[0] == "l":
                    p1, p2 = item[1], item[2]
                    dx, dy = p2.x - p1.x, p2.y - p1.y
                    length = (dx * dx + dy * dy) ** 0.5
                    if length >= 500 and abs(dx) < 2:
                        vertical_lines.append(
                            (float((p1.x + p2.x) / 2), float(min(p1.y, p2.y)),
                             float(max(p1.y, p2.y)), length)
                        )
                    if length >= 500 and abs(dy) < 2:
                        horizontal_lines.append(
                            (float(min(p1.x, p2.x)), float((p1.y + p2.y) / 2),
                             float(max(p1.x, p2.x)), length)
                        )

        panels = []
        candidates = []
        for panel in titles:
            cx = (panel["bbox"][0] + panel["bbox"][2]) / 2.0
            left = [
                line for line in vertical_lines
                if line[0] < cx and line[1] < 400 and line[2] > 900
            ]
            right = [
                line for line in vertical_lines
                if line[0] > cx and line[1] < 400 and line[2] > 900
            ]
            left_line = min(left, key=lambda line: abs(line[0] - cx), default=None)
            right_line = min(right, key=lambda line: abs(line[0] - cx), default=None)
            if left_line and right_line:
                x0 = left_line[0]
                x1 = right_line[0]
                y0 = min(left_line[1], right_line[1])
                y1 = max(left_line[2], right_line[2])
            else:
                x0 = max(0.0, cx - 330.0)
                x1 = min(float(page.rect.width), cx + 330.0)
                y0 = 450.0
            y1 = panel["bbox"][1] - 25.0
            evidence = [panel["evidence_id"], f"vector-frame-{panel['index']}"]
            panel_lines = sum(
                1 for line in vertical_lines
                if x0 <= line[0] <= x1 and line[1] < y1 and line[2] > y0
            )
            panel_bbox = [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]
            panels.append({
                "panel_id": f"PLAN-{panel['index']:02d}",
                "title": panel["title"],
                "bbox": panel_bbox,
                "evidence_ids": evidence,
                "vertical_frame_evidence_count": panel_lines,
                "horizontal_frame_evidence_count": sum(
                    1 for line in horizontal_lines
                    if x0 <= line[0] and line[2] <= x1 and y0 <= line[1] <= y1
                ),
            })

            # Evidence-backed candidates stay UNKNOWN until approval-grade semantics are proven.
            if panel_lines >= 2:
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-BOUNDARY-01",
                    element_type="OUTER_BOUNDARY",
                    bbox=tuple(panel_bbox),
                    confidence=0.90,
                    evidence_ids=(panel["evidence_id"], f"vector-frame-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Plan frame is evidenced by long vector lines, but architectural boundary semantics are not independently verified.",
                ))
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-FORM-01",
                    element_type="OVERALL_PLAN_FORM",
                    bbox=tuple(panel_bbox),
                    confidence=0.88,
                    evidence_ids=(panel["evidence_id"], f"vector-frame-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Plan extent is evidenced, but overall architectural form is not independently verified.",
                ))
                candidates.append(LockedElementCandidate(
                    candidate_id=f"{panel['index']:02d}-WALLS-01",
                    element_type="WALLS",
                    bbox=tuple(panel_bbox),
                    confidence=0.72,
                    evidence_ids=(panel["evidence_id"], f"vector-wall-lines-{panel['index']}"),
                    status="UNKNOWN",
                    rationale="Long vector linework is consistent with walls, but wall semantics are not proven.",
                ))

            square_count = 0
            for drawing_index, rect in filled_rects:
                if x0 <= rect.x0 <= x1 and y0 <= rect.y0 <= y1:
                    square_count += 1
                    if square_count <= 12:
                        candidates.append(LockedElementCandidate(
                            candidate_id=f"{panel['index']:02d}-FIXED-{square_count:02d}",
                            element_type="COLUMNS",
                            bbox=(round(rect.x0, 2), round(rect.y0, 2),
                                  round(rect.x1, 2), round(rect.y1, 2)),
                            confidence=0.62,
                            evidence_ids=(panel["evidence_id"], f"pdf-drawing-{drawing_index}"),
                            status="UNKNOWN",
                            rationale="Near-square filled vector mark detected, but its architectural semantics are not proven.",
                        ))

        for candidate in candidates:
            candidate.validate()

        missing = [element_type for element_type in _FIXED_TYPES
                   if not any(c.element_type == element_type and c.status == "LOCKED"
                              for c in candidates)]
        return {
            "detector_id": self.detector_id,
            "status": "UNKNOWN" if missing else "ACCESSIBLE",
            "source_sha256": source_sha256,
            "page_count": document.page_count,
            "plan_panels": panels,
            "candidates": [candidate.__dict__ for candidate in candidates],
            "locked_element_types": [],
            "unresolved_fixed_element_types": missing,
            "reason": (
                "Vector evidence identifies plan panels and fixed-element candidates, "
                "but does not prove approval-grade semantics for columns/walls/doors/windows."
            ) if missing else "All fixed element types identified at approval-grade confidence.",
        }

    def _raster_fallback(self, source_sha256: str) -> dict[str, Any]:
        return {
            "detector_id": self.detector_id,
            "status": "UNKNOWN",
            "source_sha256": source_sha256,
            "plan_panels": [],
            "candidates": [],
            "locked_element_types": [],
            "unresolved_fixed_element_types": list(_FIXED_TYPES),
            "reason": "Raster-only input lacks approval-grade semantic evidence for fixed elements.",
        }
