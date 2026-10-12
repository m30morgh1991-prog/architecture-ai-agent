from __future__ import annotations
import hashlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from runtime.dwg_semantic_evidence import extract_dwg_evidence

class _Dxf(dict): pass
class _Entity:
    def __init__(self, dxftype, handle, **values):
        self.dxftype, self.handle, self.dxf = dxftype, handle, _Dxf(values)
    def get_points(self, code="xy"):
        return self.dxf.get("vertices", [])

class _Layout:
    def __init__(self, entities): self.entities = entities
    def query(self, types=None): return iter(self.entities)

class _Doc:
    version="AC1021"; decode_version="AC1021"; units="millimeters"
    def __init__(self, entities, insunits=None):
        self.layout=_Layout(entities)
        self.insunits=insunits
    def modelspace(self): return self.layout
    def header_variables(self):
        return {"extmin":(0,0,0),"extmax":(100,100,0),"insunits":self.insunits}

class _Ezdwg:
    def __init__(self, doc): self.doc=doc
    def read(self, path): return self.doc

class TestDwgGeometryEvidence(unittest.TestCase):
    def test_line_coordinates_are_direct_evidence_not_semantics(self):
        doc=_Doc([_Entity("LINE",1,layer="A-GENERIC",start=(1,2,0),end=(8,2,0))])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"sample.dwg"; source.write_bytes(b"fixture")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        line=result["geometry"][0]
        self.assertEqual(line["start"],{"x":1.0,"y":2.0,"z":0.0})
        self.assertEqual(line["end"],{"x":8.0,"y":2.0,"z":0.0})
        self.assertEqual(line["coordinate_status"],"SUPPORTED")
        self.assertFalse(line["semantic_authority"])
        self.assertEqual(result["semantic_candidates"]["WALLS"]["status"],"UNKNOWN")
        self.assertEqual(result["source_profile"]["sha256"],hashlib.sha256(b"fixture").hexdigest())

    def test_polyline_vertices_are_preserved_without_classification(self):
        doc=_Doc([_Entity("LWPOLYLINE",2,layer="0",vertices=[(0,0),(10,0),(10,5),(0,5)],closed=True)])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"polyline.dwg"; source.write_bytes(b"polyline")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        poly=result["geometry"][0]
        self.assertEqual(len(poly["vertices"]),4)
        self.assertTrue(poly["closed"])
        self.assertEqual(poly["coordinate_status"],"SUPPORTED")
        self.assertEqual(result["semantic_candidates"]["WALLS"]["status"],"UNKNOWN")


    def test_raw_insunits_is_separate_from_parser_reported_units(self):
        doc=_Doc([_Entity("LINE",4,layer="0",start=(0,0,0),end=(10,0,0))],insunits=5)
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"units.dwg"; source.write_bytes(b"units")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["units_evidence"]["raw_insunits_code"],5)
        self.assertEqual(result["units_evidence"]["declared_units"],"centimeters")
        self.assertEqual(result["units_evidence"]["units_metadata_source"],"ezdwg.header_variables().insunits")
        self.assertEqual(result["units_evidence"]["parser_reported_units"],"millimeters")
        self.assertEqual(result["units_evidence"]["declared_units_metadata_status"],"NEEDS_REVIEW")
        self.assertEqual(result["units_evidence"]["effective_units_status"],"NEEDS_REVIEW")
        self.assertEqual(result["units_evidence"]["plot_scale_status"],"UNKNOWN")

    def test_missing_insunits_remains_unknown_even_if_parser_has_unit_label(self):
        doc=_Doc([_Entity("LINE",5,layer="0",start=(0,0,0),end=(1,0,0))])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"no-insunits.dwg"; source.write_bytes(b"no-insunits")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertIsNone(result["units_evidence"]["raw_insunits_code"])
        self.assertIsNone(result["units_evidence"]["declared_units"])
        self.assertEqual(result["units_evidence"]["declared_units_metadata_status"],"UNKNOWN")
        self.assertEqual(result["units_evidence"]["effective_units_status"],"UNKNOWN")
        self.assertTrue(result["units_evidence"]["human_review_required"])


    def test_matching_header_and_parser_label_still_needs_geometry_scale_review(self):
        doc=_Doc([_Entity("LINE",6,layer="0",start=(0,0,0),end=(10,0,0))],insunits=4)
        doc.units="millimeters"
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"matching-units.dwg"; source.write_bytes(b"matching-units")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        units=result["units_evidence"]
        self.assertEqual(units["declared_units_metadata_status"],"SUPPORTED")
        self.assertEqual(units["effective_units_status"],"NEEDS_REVIEW")
        self.assertTrue(units["human_review_required"])

    def test_missing_coordinates_stay_unknown(self):
        doc=_Doc([_Entity("LINE",3,layer="A-GENERIC")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"empty.dwg"; source.write_bytes(b"empty")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["geometry"][0]["coordinate_status"],"UNKNOWN")
        self.assertFalse(result["authority"]["semantic_authority"])


    def test_partial_geometry_does_not_claim_supported_coordinates(self):
        entities = [
            _Entity("LINE", 7, layer="0", start=(1, 2, 0)),
            _Entity("CIRCLE", 8, layer="0", center=(3, 4, 0)),
        ]
        doc = _Doc(entities)
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "partial.dwg"
            source.write_bytes(b"partial")
            with patch.dict("sys.modules", {"ezdwg": _Ezdwg(doc)}):
                result = extract_dwg_evidence(source)
        self.assertEqual([row["coordinate_status"] for row in result["geometry"]],
                         ["UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN"])

    def test_non_finite_geometry_values_remain_unknown(self):
        entities = [
            _Entity("LINE", 9, layer="0", start=(float("nan"), 2, 0), end=(8, 2, 0)),
            _Entity("CIRCLE", 10, layer="0", center=(3, 4, 0), radius=float("inf")),
            _Entity("LWPOLYLINE", 11, layer="0",
                    vertices=[(0, 0), (float("nan"), 3), (5, 5)], closed=True),
            _Entity("SPLINE", 12, layer="0",
                    control_points=[(0, 0, 0), (float("inf"), 2, 0)], degree=2, closed=False),
        ]
        doc = _Doc(entities)
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "non-finite.dwg"
            source.write_bytes(b"non-finite")
            with patch.dict("sys.modules", {"ezdwg": _Ezdwg(doc)}):
                result = extract_dwg_evidence(source)
        self.assertEqual([row["coordinate_status"] for row in result["geometry"]],
                         ["UNKNOWN", "UNKNOWN"])
        self.assertIsNone(result["geometry"][0]["start"])
        self.assertIsNone(result["geometry"][1]["radius"])
        self.assertEqual(result["geometry"][2]["coordinate_status"], "UNKNOWN")
        self.assertEqual(result["geometry"][2]["vertices"], [])
        self.assertEqual(result["geometry"][3]["coordinate_status"], "UNKNOWN")
        self.assertEqual(result["geometry"][3]["control_points"], [])

if __name__=="__main__": unittest.main()
