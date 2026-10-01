import unittest
from runtime.opening_connectivity import classify_opening_connectivity

class OpeningConnectivityTests(unittest.TestCase):
    def test_door_on_shared_boundary_yields_unknown_connected_by_opening(self):
        spaces=[
            {"space_id":"A","boundary_handle":"A","evidence_ids":["ea"]},
            {"space_id":"B","boundary_handle":"B","evidence_ids":["eb"]},
        ]
        boundaries={"A":[(0,0),(10,0),(10,10),(0,10)],"B":[(10,0),(20,0),(20,10),(10,10)]}
        openings=[{"opening_id":"D1","point":[10,5],"evidence_id":"ed1"}]
        r=classify_opening_connectivity(openings,spaces,boundaries,tolerance=0.01)
        self.assertEqual(r[0]["type"],"CONNECTED_BY_OPENING")
        self.assertEqual(r[0]["status"],"UNKNOWN")

    def test_unresolved_door_never_gets_fake_connection(self):
        spaces=[{"space_id":"A","boundary_handle":"A","evidence_ids":["ea"]}]
        boundaries={"A":[(0,0),(10,0),(10,10),(0,10)]}
        openings=[{"opening_id":"D1","point":[5,5],"evidence_id":"ed1"}]
        r=classify_opening_connectivity(openings,spaces,boundaries,tolerance=0.01)
        self.assertEqual(r[0]["type"],"OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(r[0]["status"],"UNKNOWN")

if __name__ == "__main__": unittest.main()
