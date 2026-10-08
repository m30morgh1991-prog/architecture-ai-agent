from __future__ import annotations
import hashlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from runtime.dwg_semantic_evidence import extract_dwg_evidence

class _Dxf(dict): pass
class _Entity:
    def __init__(self, dxftype, handle, **values):
        self.dxftype, self.handle, self.dxf = dxftype, handle, _Dxf(values)
class _Layout:
    def __init__(self, entities): self.entities = entities
    def query(self, types=None): return iter(self.entities)
class _Doc:
    version="AC1021"; decode_version="AC1021"; units="millimeters"
    def __init__(self, entities): self.layout=_Layout(entities)
    def modelspace(self): return self.layout
    def header_variables(self): return {"extmin":(0,0,0),"extmax":(100,100,0)}
class _Ezdwg:
    def __init__(self, doc): self.doc=doc
    def read(self, path): return self.doc

class TestDwgSemanticEvidence(unittest.TestCase):
    def test_direct_names_are_supported_but_generic_geometry_is_not(self):
        doc=_Doc([_Entity("LINE",1,layer="A-WALL"),_Entity("LINE",2,layer="A-GENERIC"),
                  _Entity("INSERT",3,layer="A-GENERIC",name="DOOR_SINGLE"),
                  _Entity("TEXT",4,layer="A-TEXT",text="پذیرایی"),
                  _Entity("DIMENSION",5,layer="A-DIMS",text="300",actual_measurement=300.0)])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"sample.dwg"; source.write_bytes(b"fixture")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["source_profile"]["sha256"],hashlib.sha256(b"fixture").hexdigest())
        self.assertEqual(result["entity_counts"]["LINE"],2)
        self.assertEqual(result["semantic_candidates"]["WALLS"]["status"],"SUPPORTED")
        self.assertEqual(result["semantic_candidates"]["DOORS"]["status"],"SUPPORTED")
        self.assertEqual(result["semantic_candidates"]["WINDOWS"]["status"],"UNKNOWN")
        self.assertEqual(result["semantic_candidates"]["COLUMNS"]["status"],"UNKNOWN")
        self.assertTrue(result["authority"]["generic_linework_is_not_architectural_truth"])
        self.assertEqual(result["text"][0]["provenance"],"DIRECT")
        self.assertEqual(result["dimensions"][0]["actual_measurement"],300.0)

    def test_explicit_level_code_becomes_direct_level_evidence(self):
        doc=_Doc([_Entity("TEXT",10,layer="A-LEVEL",text="کد ارتفاعی +0.15m")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"sample.dwg"; source.write_bytes(b"level")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(len(result["levels"]), 1)
        self.assertEqual(result["levels"][0]["status"], "SUPPORTED")
        self.assertEqual(result["levels"][0]["elevation"], 0.15)
        self.assertEqual(result["levels"][0]["unit"], "m")
        self.assertEqual(result["levels"][0]["provenance"], "DIRECT")
        self.assertEqual(result["levels"][0]["source_sha256"], hashlib.sha256(b"level").hexdigest())

    def test_uncontextualized_number_is_not_promoted_to_level(self):
        doc=_Doc([_Entity("TEXT",11,layer="A-NOTES",text="300")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"sample.dwg"; source.write_bytes(b"unknown-level")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["levels"][0]["status"] if result["levels"] else "NONE", "UNKNOWN")

    def test_section_marker_text_is_source_bound_but_direction_and_cut_plane_stay_unknown(self):
        doc=_Doc([_Entity("TEXT",12,layer="A-ANNOTATION",text="مقطع A-A →")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"section.dwg"; source.write_bytes(b"section-marker")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(len(result["section_markers"]), 1)
        marker=result["section_markers"][0]
        self.assertEqual(marker["marker_type"], "SECTION_MARKER")
        self.assertEqual(marker["label"], "A-A")
        self.assertEqual(marker["status"], "SUPPORTED")
        self.assertEqual(marker["direction_status"], "UNKNOWN")
        self.assertEqual(marker["cut_plane_status"], "UNKNOWN")
        self.assertEqual(marker["source_sha256"], hashlib.sha256(b"section-marker").hexdigest())

    def test_bare_section_like_label_is_not_promoted_without_context(self):
        doc=_Doc([_Entity("TEXT",13,layer="A-NOTES",text="A-A")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"bare-label.dwg"; source.write_bytes(b"bare-label")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["section_markers"], [])

    def test_explicit_section_block_name_is_candidate_not_direction_truth(self):
        doc=_Doc([_Entity("INSERT",14,layer="A-SYMBOL",name="SECTION_MARKER_AA")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"section-block.dwg"; source.write_bytes(b"section-block")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(len(result["section_markers"]), 1)
        self.assertEqual(result["section_markers"][0]["evidence_kind"], "BLOCK")
        self.assertEqual(result["section_markers"][0]["direction_status"], "UNKNOWN")
        self.assertFalse(result["authority"]["semantic_authority"])

    def test_missing_direct_semantic_evidence_stays_unknown(self):
        doc=_Doc([_Entity("LINE",1,layer="A-GENERIC")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"sample.dwg"; source.write_bytes(b"fixture")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        for semantic in ("WALLS","DOORS","WINDOWS","COLUMNS"):
            self.assertEqual(result["semantic_candidates"][semantic]["status"],"UNKNOWN")

if __name__=="__main__": unittest.main()
