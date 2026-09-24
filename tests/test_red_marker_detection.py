import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from runtime.red_marker_detection import RedStructuralMarkerDetector


class RedMarkerDetectionTests(unittest.TestCase):
    def test_detects_realistic_red_marker_grid_without_assigning_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.jpg"
            image = np.full((984, 1536, 3), 255, dtype=np.uint8)
            points = [(141,205),(419,205),(700,205),(1048,205),(1321,205),
                      (141,531),(419,531),(700,621),(1048,621),(1321,621),
                      (141,809),(419,812),(700,809),(1048,809),(1321,812)]
            for x, y in points:
                cv2.circle(image, (x, y), 8, (0, 0, 255), -1)
            cv2.imwrite(str(path), image)

            result = RedStructuralMarkerDetector().detect(str(path), "sha-test")

            self.assertEqual(result["status"], "EVIDENCE_AVAILABLE")
            self.assertEqual(result["marker_count"], 15)
            self.assertEqual(len(result["grid_x_centers"]), 5)
            self.assertEqual(len(result["grid_y_centers"]), 4)
            self.assertEqual(result["architectural_semantics"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
