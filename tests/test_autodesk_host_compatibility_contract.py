from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "adapters" / "autodesk" / "AIE.Autodesk.ReadOnlyExtractor.csproj"
SOURCE = ROOT / "adapters" / "autodesk" / "AIEReadOnlyExtractor.cs"
README = ROOT / "adapters" / "autodesk" / "README.md"
CONTRACT = ROOT / "docs" / "aie" / "AUTODESK_ADAPTER_CONTRACT.md"


class AutodeskHostCompatibilityContractTests(unittest.TestCase):
    def test_project_declares_both_supported_host_frameworks(self):
        root = ET.parse(PROJECT).getroot()
        frameworks = root.findtext("PropertyGroup/TargetFrameworks")
        self.assertEqual(frameworks, "net47;net8.0-windows")

    def test_autodesk_host_assemblies_are_not_copied_to_plugin_output(self):
        root = ET.parse(PROJECT).getroot()
        refs = {node.attrib["Include"]: node for node in root.findall(".//Reference")}
        for name in ("AcCoreMgd", "AcDbMgd", "AcMgd"):
            self.assertIn(name, refs)
            self.assertEqual(refs[name].findtext("Private"), "false")

    def test_framework_compatible_json_and_sha256_apis_are_used(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("Newtonsoft.Json", source)
        self.assertIn("JsonConvert.SerializeObject", source)
        self.assertNotIn("System.Text.Json", source)
        self.assertNotIn("Convert.ToHexString", source)

    def test_extractor_remains_read_only_and_fail_closed(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("OpenMode.ForRead", source)
        self.assertIn("doc.IsModified", source)
        self.assertIn('snapshot_binding_status"] = "NEEDS_REVIEW"', source)
        self.assertIn("source_mutated"] = false", source)
        self.assertNotIn("doc.Save(", source)
        self.assertNotIn("db.SaveAs(", source)

    def test_host_build_requirements_and_limits_are_documented(self):
        readme = README.read_text(encoding="utf-8")
        contract = CONTRACT.read_text(encoding="utf-8")
        self.assertIn(".NET Framework 4.7", readme)
        self.assertIn("AutoCAD 2020", readme)
        self.assertIn("AutoCAD 2020", contract)
        self.assertIn("smoke test", contract.lower())


if __name__ == "__main__":
    unittest.main()
