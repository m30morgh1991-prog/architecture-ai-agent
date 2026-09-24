"""Red structural-marker evidence for plan images.

Markers are treated as geometric evidence only. They are never assumed to be
columns without independent architectural proof.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np


@dataclass(frozen=True)
class RedMarker:
    marker_id: str
    center: tuple[float, float]
    bbox: tuple[int, int, int, int]
    area: int
    grid_x: int | None
    grid_y: int | None
    confidence: float

    def validate(self) -> None:
        if not self.marker_id or self.area <= 0:
            raise ValueError("INVALID_RED_MARKER")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("INVALID_MARKER_CONFIDENCE")


class RedStructuralMarkerDetector:
    detector_id = "red-structural-marker-v0.1"

    def detect(self, source_path: str, source_sha256: str) -> dict:
        path = Path(source_path)
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            return {
                "status": "NOT_APPLICABLE",
                "source_sha256": source_sha256,
                "marker_count": 0,
                "markers": [],
                "reason": "Red-marker detection applies to raster plan images.",
            }

        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("SOURCE_DOCUMENT_UNREADABLE")
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
        mask |= cv2.inRange(hsv, np.array([170, 100, 100]), np.array([179, 255, 255]))
        count, labels, stats, centers = cv2.connectedComponentsWithStats(mask, 8)

        raw = []
        for i in range(1, count):
            x, y, w, h, area = [int(v) for v in stats[i]]
            if area < 20:
                continue
            raw.append((x, y, w, h, area, centers[i]))

        raw.sort(key=lambda item: (item[5][1], item[5][0]))
        xs = []
        ys = []
        for item in raw:
            xs.append(float(item[5][0]))
            ys.append(float(item[5][1]))

        def cluster(values: list[float], tolerance: float = 35.0) -> list[float]:
            groups: list[list[float]] = []
            for value in sorted(values):
                if not groups or abs(value - np.mean(groups[-1])) > tolerance:
                    groups.append([value])
                else:
                    groups[-1].append(value)
            return [float(np.mean(group)) for group in groups]

        x_centers = cluster(xs)
        y_centers = cluster(ys)

        markers = []
        for idx, (x, y, w, h, area, center) in enumerate(raw, 1):
            cx, cy = float(center[0]), float(center[1])
            gx = min(range(len(x_centers)), key=lambda i: abs(x_centers[i] - cx)) + 1 if x_centers else None
            gy = min(range(len(y_centers)), key=lambda i: abs(y_centers[i] - cy)) + 1 if y_centers else None
            marker = RedMarker(
                marker_id=f"RM-{idx:02d}",
                center=(round(cx, 2), round(cy, 2)),
                bbox=(x, y, w, h),
                area=area,
                grid_x=gx,
                grid_y=gy,
                confidence=0.99,
            )
            marker.validate()
            markers.append(marker)

        # Grid mapping is geometric only: it does not label a marker as a column.
        status = "EVIDENCE_AVAILABLE" if len(markers) >= 3 else "UNKNOWN"
        return {
            "detector_id": self.detector_id,
            "status": status,
            "source_sha256": source_sha256,
            "image_dimensions": [int(image.shape[1]), int(image.shape[0])],
            "marker_count": len(markers),
            "grid_x_centers": [round(v, 2) for v in x_centers],
            "grid_y_centers": [round(v, 2) for v in y_centers],
            "markers": [m.__dict__ for m in markers],
            "architectural_semantics": "UNKNOWN",
            "reason": (
                "Red markers are high-confidence visual features. Their architectural "
                "meaning remains UNKNOWN until corroborated by wall/vector/grid evidence."
            ),
        }
