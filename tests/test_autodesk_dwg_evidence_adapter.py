from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from runtime.autodesk_dwg_evidence_adapter import inspect_autodesk_export


class AutodeskDwgEvidenceAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "fixture.dwg"
        self.source.write_bytes(b"immutable-dwg-fixture")
        self.sha = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.export = self.root / "evidence.json"

    def envelope(self):
        return {
            "schema": "autodesk-autocad-readonly-evidence-v1",
            "source_profile": {"path": str(self.source), "sha256": self.sha, "insunits": "Millimeters", "coordinate_frame": "WCS_WITH_POLYLINE_OCS_DECLARED"},
            "source_integrity": {"sha256_before": self.sha, "sha256_after": self.sha, "source_mutated": False, "snapshot_binding_status": "NEEDS_REVIEW"},
            "scope": {"space": "MODEL", "entity_count": 1},
            "layers": [{"name": "A-WALL"}],
            "entities": [{"handle": "2A", "type": "Line", "layer": "A-WALL", "geometry": {"kind": "LINE"}}],
            "authority": {"read_only": True, "semantic_authority": False, "compliance_assessed": False},
        }

    def write_export(self, data=None):
        self.export.write_text(json.dumps(data or self.envelope()), encoding="utf-8")

    def test_valid_export_is_bound_but_snapshot_stays_needs_review(self):
        self.write_export()
        result = inspect_autodesk_export(self.export, self.source)
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.source_sha256, self.sha)
        self.assertEqual(result.payload["semantic_promotion"], "NOT_PERMITTED")
        self.assertEqual(result.payload["snapshot_binding_assessment"], "UNVERIFIED_EXPORTER_CLAIM_IGNORED")
        result.validate(self.sha)

    def test_exporter_verified_claim_cannot_promote_snapshot_to_ready(self):
        data = self.envelope()
        data["source_integrity"]["snapshot_binding_status"] = "VERIFIED"
        self.write_export(data)
        result = inspect_autodesk_export(self.export, self.source)
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.payload["snapshot_binding_assessment"], "UNVERIFIED_EXPORTER_CLAIM_IGNORED")

    def test_changed_source_blocks(self):
        data = self.envelope()
        self.source.write_bytes(b"changed")
        self.write_export(data)
        result = inspect_autodesk_export(self.export, self.source)
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.payload["error"], "AUTODESK_SOURCE_SHA_MISMATCH")

    def test_changed_before_after_hash_blocks(self):
        data = self.envelope()
        data["source_integrity"]["sha256_after"] = "f" * 64
        self.write_export(data)
        self.assertEqual(inspect_autodesk_export(self.export, self.source).status, "BLOCKED")

    def test_source_mutation_claim_blocks(self):
        data = self.envelope()
        data["source_integrity"]["source_mutated"] = True
        self.write_export(data)
        self.assertEqual(inspect_autodesk_export(self.export, self.source).status, "BLOCKED")

    def test_semantic_authority_claim_blocks(self):
        data = self.envelope()
        data["authority"]["semantic_authority"] = True
        self.write_export(data)
        self.assertEqual(inspect_autodesk_export(self.export, self.source).status, "BLOCKED")

    def test_unitless_source_stays_needs_review(self):
        data = self.envelope()
        data["source_profile"]["insunits"] = "Unitless"
        self.write_export(data)
        self.assertEqual(inspect_autodesk_export(self.export, self.source).status, "NEEDS_REVIEW")

    def test_malformed_entity_blocks(self):
        data = self.envelope()
        data["entities"] = [{"handle": "2A", "type": "Line"}]
        self.write_export(data)
        self.assertEqual(inspect_autodesk_export(self.export, self.source).status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
