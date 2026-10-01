import unittest
from runtime.opening_connectivity import classify_opening_connectivity


class OpeningConnectivityTests(unittest.TestCase):
    def test_insertion_point_alone_never_approves_connection(self):
        spaces=[
            {"space_id":"A","boundary_handle":"A","evidence_ids":["ea"]},
            {"space_id":"B","boundary_handle":"B","evidence_ids":["eb"]},
        ]
        boundaries={
            "A":[(0,0),(10,0),(10,10),(0,10)],
            "B":[(10,0),(20,0),(20,10),(10,10)],
        }
        openings=[{"opening_id":"D1","point":[10,5],"evidence_id":"ed1"}]
        r=classify_opening_connectivity(openings,spaces,boundaries,tolerance=0.01)
        self.assertEqual(r[0]["type"],"OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(r[0]["status"],"UNKNOWN")

    def test_span_and_host_wall_evidence_yield_unknown_connected_by_opening(self):
        spaces=[
            {"space_id":"A","boundary_handle":"A","evidence_ids":["ea"]},
            {"space_id":"B","boundary_handle":"B","evidence_ids":["eb"]},
        ]
        boundaries={
            "A":[(0,0),(10,0),(10,10),(0,10)],
            "B":[(10,0),(20,0),(20,10),(10,10)],
        }
        openings=[{
            "opening_id":"D2",
            "point":[10,5],
            "span":[[10,4],[10,6]],
            "evidence_id":"ed2",
            "span_evidence_id":"span-d2",
            "host_wall_id":"W1",
            "host_wall_evidence_id":"wall-d2",
        }]
        r=classify_opening_connectivity(
            openings,spaces,boundaries,tolerance=0.01,host_wall_ids={"W1"}
        )
        self.assertEqual(r[0]["type"],"CONNECTED_BY_OPENING")
        self.assertEqual(r[0]["status"],"UNKNOWN")
        self.assertIn("span-d2",r[0]["evidence_ids"])
        self.assertIn("wall-d2",r[0]["evidence_ids"])

    def test_missing_host_wall_evidence_stays_unknown(self):
        spaces=[
            {"space_id":"A","boundary_handle":"A","evidence_ids":["ea"]},
            {"space_id":"B","boundary_handle":"B","evidence_ids":["eb"]},
        ]
        boundaries={
            "A":[(0,0),(10,0),(10,10),(0,10)],
            "B":[(10,0),(20,0),(20,10),(10,10)],
        }
        openings=[{
            "opening_id":"D3","point":[10,5],"span":[[10,4],[10,6]],
            "evidence_id":"ed3","span_evidence_id":"span-d3"
        }]
        r=classify_opening_connectivity(openings,spaces,boundaries,tolerance=0.01)
        self.assertEqual(r[0]["type"],"OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(r[0]["status"],"UNKNOWN")


if __name__ == "__main__":
    unittest.main()
