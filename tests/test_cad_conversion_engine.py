from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.cad_conversion import (
    CadConversionEngine,
    CadConversionProvider,
    ConversionError,
    ConversionResult,
    ODAFileConverter,
)
from runtime.cad_conversion.oda_file_converter import sha256_file


class FakeProvider:
    provider_id = "fake_provider"

    def __init__(self, *, fidelity_status="UNKNOWN", requires_review=True, wrong_hash=False, wrong_source_hash=False, mutate_source=False):
        self.fidelity_status = fidelity_status
        self.requires_review = requires_review
        self.wrong_hash = wrong_hash
        self.wrong_source_hash = wrong_source_hash
        self.mutate_source = mutate_source

    def convert_dwg_to_dxf(self, source_path, output_path):
        source = Path(source_path)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"synthetic DXF artifact")
        if self.mutate_source:
            source.write_bytes(source.read_bytes() + b"-mutated")
        return ConversionResult(
            source_path=source,
            output_path=output,
            engine="fake",
            output_version="ACAD2018",
            source_sha256="f" * 64 if self.wrong_source_hash else sha256_file(source),
            output_sha256="0" * 64 if self.wrong_hash else sha256_file(output),
            source_unchanged=not self.mutate_source,
            execution_status="COMPLETED",
            fidelity_status=self.fidelity_status,
            requires_review=self.requires_review,
        )


class TestCadConversionEngine(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "plan.dwg"
        self.source.write_bytes(b"original DWG")
        self.output = self.root / "out" / "plan.dxf"

    def tearDown(self):
        self.temp.cleanup()

    def test_oda_adapter_implements_provider_contract(self):
        self.assertIsInstance(ODAFileConverter(), CadConversionProvider)
        self.assertEqual(ODAFileConverter().provider_id, "oda_file_converter")

    def test_explicit_provider_selection_and_success_contract(self):
        engine = CadConversionEngine([FakeProvider()])
        result = engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(engine.available_providers(), ("fake_provider",))
        self.assertEqual(result.execution_status, "COMPLETED")
        self.assertEqual(result.fidelity_status, "UNKNOWN")
        self.assertTrue(result.requires_review)
        self.assertEqual(self.source.read_bytes(), b"original DWG")

    def test_provider_is_never_selected_implicitly_or_fallback_used(self):
        engine = CadConversionEngine([FakeProvider()])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("autocad_core_console", self.source, self.output)
        self.assertEqual(caught.exception.code, "PROVIDER_UNAVAILABLE")
        self.assertFalse(self.output.exists())

    def test_empty_provider_selection_is_rejected(self):
        engine = CadConversionEngine([FakeProvider()])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("", self.source, self.output)
        self.assertEqual(caught.exception.code, "PROVIDER_REQUIRED")

    def test_provider_cannot_claim_fidelity_pass_in_v01(self):
        engine = CadConversionEngine([FakeProvider(fidelity_status="PASS", requires_review=False)])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(caught.exception.code, "PROVIDER_FIDELITY_CONTRACT_VIOLATION")

    def test_provider_output_hash_must_match_artifact(self):
        engine = CadConversionEngine([FakeProvider(wrong_hash=True)])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(caught.exception.code, "PROVIDER_OUTPUT_HASH_MISMATCH")

    def test_provider_source_hash_must_match_engine_snapshot(self):
        engine = CadConversionEngine([FakeProvider(wrong_source_hash=True)])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(caught.exception.code, "PROVIDER_SOURCE_HASH_MISMATCH")

    def test_source_mutation_is_rejected(self):
        engine = CadConversionEngine([FakeProvider(mutate_source=True)])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(caught.exception.code, "SOURCE_MUTATED")

    def test_duplicate_provider_registration_is_rejected(self):
        with self.assertRaises(ValueError):
            CadConversionEngine([FakeProvider(), FakeProvider()])

    def test_existing_output_is_not_overwritten(self):
        self.output.parent.mkdir()
        self.output.write_bytes(b"preserve")
        engine = CadConversionEngine([FakeProvider()])
        with self.assertRaises(ConversionError) as caught:
            engine.convert_dwg_to_dxf("fake_provider", self.source, self.output)
        self.assertEqual(caught.exception.code, "OUTPUT_ALREADY_EXISTS")
        self.assertEqual(self.output.read_bytes(), b"preserve")


if __name__ == "__main__":
    unittest.main()
