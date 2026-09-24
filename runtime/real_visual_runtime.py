"""Real visual artifact ingestion and fail-closed runtime execution."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import re

import cv2
import fitz
import numpy as np

from .visual_evidence import VisualEvidence
from .locked_element_detection import ConservativeLockedElementDetector
from .red_marker_detection import RedStructuralMarkerDetector
from .visual_semantic_corroboration import VisualSemanticCorroborationGate
from .plan_model_contract import ConstraintMap, PlanElement, PlanModel

_SUPPORTED = {".jpg":"JPG",".jpeg":"JPG",".png":"PNG",".webp":"WEBP",".pdf":"PDF"}
_SPACE_TERMS = re.compile(
    r"(?i)\b(COCINA|COMEDOR|SALA|ESTUDIO|HALL|SS\.?HH\.?|LAVANDERIA|DEPOSITO|"
    r"DORM(?:ITORIO)?(?:\.?\s+(?:01|02|03|HIJA|HIJO|PRINCIP\.?|SERV\.?)?)?|"
    r"TERRAZA|JARDIN(?:\s+INTERIOR\s+\d|\s+EXTERIOR\s+\d)?|AZOTEA|ESTACIONAMIENTO)\b"
)

@dataclass(frozen=True)
class VisualArtifact:
    source_path: str
    input_type: str
    sha256: str
    width: int
    height: int
    page_count: int
    image: Any

class RealVisualArtifactAdapter:
    """Concrete visual adapter for real local JPG/PNG/WEBP/PDF artifacts."""
    adapter_id = "real-opencv-pymupdf-v0.1"

    def ingest(self, source_path: str) -> VisualArtifact:
        path = Path(source_path)
        input_type = _SUPPORTED.get(path.suffix.lower())
        if input_type is None:
            raise ValueError("UNSUPPORTED_VISUAL_INPUT")
        if not path.is_file():
            raise ValueError("SOURCE_DOCUMENT_MISSING")
        raw = path.read_bytes()
        digest = sha256(raw).hexdigest()
        if input_type == "PDF":
            document = fitz.open(stream=raw, filetype="pdf")
            if document.page_count == 0:
                raise ValueError("SOURCE_DOCUMENT_EMPTY")
            pixmap = document[0].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            array = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
                pixmap.height, pixmap.width, pixmap.n
            )
            image = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            return VisualArtifact(
                str(path), input_type, digest, pixmap.width, pixmap.height,
                document.page_count, image
            )
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("SOURCE_DOCUMENT_UNREADABLE")
        height, width = image.shape[:2]
        return VisualArtifact(str(path), input_type, digest, width, height, 1, image)

    def detect(self, artifact: VisualArtifact) -> dict[str, Any]:
        gray = cv2.cvtColor(artifact.image, cv2.COLOR_BGR2GRAY)
        scale = min(1.0, 1800.0 / max(gray.shape[1], 1))
        small = cv2.resize(gray, (0, 0), fx=scale, fy=scale)
        edges = cv2.Canny(small, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=60, minLineLength=35, maxLineGap=8)
        line_count = 0 if lines is None else int(len(lines))
        _, binary = cv2.threshold(gray, 205, 255, cv2.THRESH_BINARY_INV)
        _, _, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
        minimum_area = max(5000, int(artifact.width * artifact.height * 0.002))
        regions = []
        for x, y, width, height, area in stats[1:]:
            if area >= minimum_area and width > artifact.width*0.08 and height > artifact.height*0.08:
                regions.append({"bbox":[int(x),int(y),int(width),int(height)],"area":int(area)})
        regions = sorted(regions, key=lambda item:item["area"], reverse=True)[:12]
        extracted_text = ""
        if artifact.input_type == "PDF":
            document = fitz.open(artifact.source_path)
            extracted_text = "\n".join(page.get_text() for page in document)
        labels = sorted({m.group(1).upper().replace(" ","_") for m in _SPACE_TERMS.finditer(extracted_text)})
        return {
            "artifact_sha256": artifact.sha256,
            "input_type": artifact.input_type,
            "dimensions": [artifact.width, artifact.height],
            "page_count": artifact.page_count,
            "visual_line_count": line_count,
            "major_regions": regions,
            "recognized_space_labels": labels,
            "fixed_element_identification": {
                "status": "UNKNOWN",
                "reason": (
                    "Architectural linework is present, but this adapter cannot "
                    "reliably identify columns and other structural fixed elements "
                    "at approval-grade confidence."
                ),
            },
        }

class RealVisualRuntime:
    """Execute the real-artifact path and stop safely on critical uncertainty."""
    def __init__(self, adapter: RealVisualArtifactAdapter | None = None, locked_detector=None, marker_detector=None, corroboration_gate=None):
        self.adapter = adapter or RealVisualArtifactAdapter()
        self.locked_detector = locked_detector or ConservativeLockedElementDetector()
        self.marker_detector = marker_detector or RedStructuralMarkerDetector()
        self.corroboration_gate = corroboration_gate or VisualSemanticCorroborationGate()

    def _build_contracts(
        self,
        *,
        artifact: VisualArtifact,
        locked_elements: dict[str, Any],
        evidence_id: str,
    ) -> tuple[PlanModel, ConstraintMap]:
        elements: list[PlanElement] = []
        unresolved = list(locked_elements.get("unresolved_fixed_element_types", []))

        for candidate in locked_elements.get("candidates", []):
            elements.append(
                PlanElement(
                    element_id=str(candidate["candidate_id"]),
                    element_type=str(candidate["element_type"]),
                    state="LOCKED" if candidate.get("status") == "LOCKED" else "UNKNOWN",
                    geometry={"bbox": list(candidate.get("bbox", ()))},
                    evidence_ids=tuple(candidate.get("evidence_ids", ())) or (evidence_id,),
                    confidence=float(candidate.get("confidence", 0.0)),
                )
            )

        plan_model = PlanModel(
            model_id=f"plan-{artifact.sha256[:16]}",
            source_sha256=artifact.sha256,
            drawing_count=artifact.page_count,
            elements=tuple(elements),
            unresolved=tuple(unresolved),
        )
        plan_model.validate()

        locked_ids = tuple(e.element_id for e in elements if e.state == "LOCKED")
        unknown_ids = tuple(e.element_id for e in elements if e.state == "UNKNOWN")
        constraint_map = ConstraintMap(
            map_id=f"constraints-{artifact.sha256[:16]}",
            model_id=plan_model.model_id,
            protected_element_ids=locked_ids,
            editable_element_ids=(),
            conditional_element_ids=(),
            unknown_element_ids=unknown_ids,
            evidence_ids=(evidence_id,),
        )
        constraint_map.validate()
        return plan_model, constraint_map

    def run(self, execution_id: str, source_path: str, change_request: dict[str, Any]) -> dict[str, Any]:
        artifact = self.adapter.ingest(source_path)
        detection = self.adapter.detect(artifact)
        locked_elements = self.locked_detector.detect(artifact.source_path, artifact.sha256)
        marker_evidence = self.marker_detector.detect(artifact.source_path, artifact.sha256)
        corroboration = self.corroboration_gate.evaluate(
            marker_evidence=bool(marker_evidence.get("markers")),
            wall_geometry_evidence=bool(detection.get("visual_line_count", 0) > 0),
            vector_or_grid_evidence=bool(locked_elements.get("plan_panels")),
            structural_geometry_evidence=bool(locked_elements.get("candidates")),
            contradiction_evidence=False,
        )
        contract_error = None
        try:
            plan_model, constraint_map = self._build_contracts(
                artifact=artifact,
                locked_elements=locked_elements,
                evidence_id=f"real-{execution_id}",
            )
        except ValueError as exc:
            plan_model = None
            constraint_map = None
            contract_error = str(exc)

        stages = [
            "SOURCE","DETECTION","PLAN_MODEL","CONSTRAINT_MAP",
            "LOCKED_IDENTIFICATION","SEMANTIC_CORROBORATION","CHANGE_REQUEST"
        ]
        blocker = contract_error
        if blocker is None and (
            detection["fixed_element_identification"]["status"] != "ACCESSIBLE"
            or locked_elements["status"] != "ACCESSIBLE"
            or corroboration.status != "ACCESSIBLE"
        ):
            blocker = "LOCKED_ELEMENT_UNCERTAIN"
        evidence = VisualEvidence(
            evidence_id=f"real-{execution_id}",
            input_type=artifact.input_type,
            stages=stages,
        )
        evidence.validate()
        return {
            "execution_id": execution_id,
            "status": "BLOCKED" if blocker else "READY_FOR_APPROVAL",
            "blockers": [blocker] if blocker else [],
            "contracts": {
                "status": "BLOCKED" if contract_error else "VALID",
                "plan_model_id": plan_model.model_id if plan_model else None,
                "constraint_map_id": constraint_map.map_id if constraint_map else None,
                "element_count": len(plan_model.elements) if plan_model else 0,
                "unresolved": list(plan_model.unresolved) if plan_model else [],
                "error": contract_error,
            },
            "constraint_map": {
                "protected_element_ids": list(constraint_map.protected_element_ids) if constraint_map else [],
                "editable_element_ids": list(constraint_map.editable_element_ids) if constraint_map else [],
                "conditional_element_ids": list(constraint_map.conditional_element_ids) if constraint_map else [],
                "unknown_element_ids": list(constraint_map.unknown_element_ids) if constraint_map else [],
                "evidence_ids": list(constraint_map.evidence_ids) if constraint_map else [],
            },
            "evidence": {
                "evidence_id": evidence.evidence_id,
                "input_type": evidence.input_type,
                "stages": evidence.stages,
                "complete": evidence.complete,
            },
            "source": {
                "path": artifact.source_path,
                "sha256": artifact.sha256,
                "width": artifact.width,
                "height": artifact.height,
                "page_count": artifact.page_count,
            },
            "detection": detection,
            "locked_element_detection": locked_elements,
            "red_marker_evidence": marker_evidence,
            "semantic_corroboration": {
                "status": corroboration.status,
                "semantics": corroboration.semantics,
                "supporting_evidence": list(corroboration.supporting_evidence),
                "contradictions": list(corroboration.contradictions),
                "reason": corroboration.reason,
            },
            "change_request": change_request,
            "next_stage": None if blocker else "APPROVED_CHANGE_PLAN",
        }
