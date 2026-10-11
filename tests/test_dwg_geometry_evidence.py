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
    def __init__(self, entities): self.layout=_Layout(entities)
    def modelspace(self): return self.layout
    def header_variables(self): return {"extmin":(0,0,0),"extmax":(100,100,0)}

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

    def test_missing_coordinates_stay_unknown(self):
        doc=_Doc([_Entity("LINE",3,layer="A-GENERIC")])
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"empty.dwg"; source.write_bytes(b"empty")
            with patch.dict("sys.modules",{"ezdwg":_Ezdwg(doc)}):
                result=extract_dwg_evidence(source)
        self.assertEqual(result["geometry"][0]["coordinate_status"],"UNKNOWN")
        self.assertFalse(result["authority"]["semantic_authority"])

if __name__=="__main__": unittest.main()
