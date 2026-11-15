from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.cad_conversion import ConversionError, ODAFileConverter, ODAFileConverterConfig


class TestODAFileConverter(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "plan.dwg"
        self.source.write_bytes(b"DWG-TEST-SOURCE")
        self.output = self.root / "out" / "plan.dxf"

    def tearDown(self):
        self.temp.cleanup()

    def _mock_success(self, command, **kwargs):
        Path(command[2], "source.dxf").write_bytes(b"DXF-TEST-OUTPUT")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run")
    def test_success_is_execution_only_and_preserves_source(self, run, _which):
        run.side_effect = self._mock_success
        original = self.source.read_bytes()
        result = ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(self.output.read_bytes(), b"DXF-TEST-OUTPUT")
        self.assertEqual(self.source.read_bytes(), original)
        self.assertTrue(result.source_unchanged)
        self.assertEqual(result.execution_status, "COMPLETED")
        self.assertEqual(result.fidelity_status, "UNKNOWN")
        self.assertTrue(result.requires_review)
        command = run.call_args.args[0]
        self.assertEqual(command[3:8], ["*.dwg", "ACAD2018", "DXF", "0", "0"])
        self.assertEqual(run.call_args.kwargs["timeout"], 300)

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run")
    def test_failed_exclusive_create_does_not_remove_concurrent_output(self, run, _which):
        run.side_effect = self._mock_success
        original_open = Path.open

        def simulate_concurrent_output(path, mode="r", *args, **kwargs):
            if path == self.output and mode == "xb":
                with original_open(path, "wb") as stream:
                    stream.write(b"created-by-another-process")
                raise PermissionError("simulated exclusive-create failure")
            return original_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", new=simulate_concurrent_output):
            with self.assertRaises(ConversionError) as caught:
                ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)

        self.assertEqual(caught.exception.code, "OUTPUT_WRITE_FAILED")
        self.assertEqual(self.output.read_bytes(), b"created-by-another-process")

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.shutil.copy2")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run")
    def test_staged_source_mismatch_is_rejected_before_converter(self, run, copy, _which):
        def write_corrupt_copy(source, destination):
            Path(destination).write_bytes(b"CORRUPTED-STAGED-DWG")

        copy.side_effect = write_corrupt_copy
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)

        self.assertEqual(caught.exception.code, "STAGED_SOURCE_MISMATCH")
        run.assert_not_called()
        self.assertFalse(self.output.exists())
        self.assertEqual(self.source.read_bytes(), b"DWG-TEST-SOURCE")

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value=None)
    def test_missing_executable_fails_closed(self, _which):
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(caught.exception.code, "CONVERTER_NOT_FOUND")

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run")
    def test_nonzero_exit_is_rejected(self, run, _which):
        run.return_value = subprocess.CompletedProcess([], 2, stdout="", stderr="failed")
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(caught.exception.code, "CONVERTER_NONZERO_EXIT")
        self.assertFalse(self.output.exists())

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run")
    def test_missing_output_is_rejected(self, run, _which):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(caught.exception.code, "OUTPUT_MISSING_OR_AMBIGUOUS")

    @patch("runtime.cad_conversion.oda_file_converter.shutil.which", return_value="/mock/ODAFileConverter")
    @patch("runtime.cad_conversion.oda_file_converter.subprocess.run", side_effect=subprocess.TimeoutExpired("oda", 1))
    def test_timeout_is_rejected(self, _run, _which):
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter(ODAFileConverterConfig(timeout_seconds=1)).convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(caught.exception.code, "CONVERSION_TIMEOUT")

    def test_existing_output_is_never_overwritten(self):
        self.output.parent.mkdir()
        self.output.write_bytes(b"keep-me")
        with self.assertRaises(ConversionError) as caught:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.output)
        self.assertEqual(caught.exception.code, "OUTPUT_ALREADY_EXISTS")
        self.assertEqual(self.output.read_bytes(), b"keep-me")

    def test_rejects_wrong_extensions(self):
        wrong_source = self.root / "plan.dxf"
        wrong_source.write_bytes(b"dxf")
        with self.assertRaises(ConversionError) as source_error:
            ODAFileConverter().convert_dwg_to_dxf(wrong_source, self.output)
        self.assertEqual(source_error.exception.code, "SOURCE_FORMAT_UNSUPPORTED")
        with self.assertRaises(ConversionError) as output_error:
            ODAFileConverter().convert_dwg_to_dxf(self.source, self.root / "plan.dwg")
        self.assertEqual(output_error.exception.code, "OUTPUT_FORMAT_INVALID")

    def test_config_rejects_unknown_version_and_invalid_timeout(self):
        with self.assertRaises(ValueError):
            ODAFileConverterConfig(timeout_seconds=0)
        with self.assertRaises(ValueError):
            ODAFileConverterConfig(output_version="LATEST")


if __name__ == "__main__":
    unittest.main()
