import unittest
from runtime.external_detection_adapter import ExternalDetectionAdapter

class ExternalDetectionAdapterTest(unittest.TestCase):
    def test_normalizes_external_entities_without_replacing_plan_model(self):
        model = ExternalDetectionAdapter().to_plan_model(
            {"elements": [
                {"id":"w1","type":"wall","geometry":{"p1":[0,0],"p2":[100,0]},"confidence":0.99},
                {"id":"r1","type":"room","geometry":{"bbox":[0,0,100,100]},"confidence":0.92},
                {"id":"f1","type":"furniture","geometry":{"bbox":[20,20,40,40]},"confidence":0.88},
            ]},
            model_id="plan-external-test", source_sha256="a"*64,
            drawing_count=1, evidence_prefix="ext-test",
        )
        self.assertEqual([e.element_type for e in model.elements], ["WALLS","SPACE","FURNITURE"])
        self.assertTrue(all(e.state == "UNKNOWN" for e in model.elements))

    def test_low_confidence_locked_external_claim_remains_unknown(self):
        model = ExternalDetectionAdapter().to_plan_model(
            {"elements":[{"id":"w1","type":"wall","state":"LOCKED",
                          "geometry":{"bbox":[0,0,10,10]},"confidence":0.80}]},
            model_id="plan-unknown-test", source_sha256="b"*64,
            drawing_count=1, evidence_prefix="ext-test",
        )
        self.assertEqual(model.elements[0].element_type, "WALLS")
        self.assertEqual(model.elements[0].state, "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
