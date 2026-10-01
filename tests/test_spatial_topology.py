import unittest
from runtime.spatial_topology import classify_space_relations

class SpatialTopologyTests(unittest.TestCase):
    def _spaces(self):
        return [
            {"space_id":"A","boundary_handle":"A","bbox":[0,0,10,10],"centroid":[5,5],"evidence_ids":["ea"]},
            {"space_id":"B","boundary_handle":"B","bbox":[10,0,20,10],"centroid":[15,5],"evidence_ids":["eb"]},
        ]

    def test_shared_boundary_requires_actual_collinear_overlap(self):
        spaces=self._spaces()
        boundaries={"A":[(0,0),(10,0),(10,10),(0,10)],"B":[(10,0),(20,0),(20,10),(10,10)]}
        r=classify_space_relations(spaces,boundaries)
        self.assertEqual(r[0]["type"],"SHARED_BOUNDARY")
        self.assertEqual(r[0]["status"],"UNKNOWN")
        self.assertGreater(r[0]["geometry_reference"]["shared_boundary_length"],0)

    def test_bbox_overlap_does_not_become_adjacency(self):
        spaces=self._spaces()
        spaces[1]["bbox"]=[5,5,15,15]
        spaces[1]["centroid"]=[10,10]
        boundaries={"A":[(0,0),(10,0),(10,10),(0,10)],"B":[(12,12),(15,12),(15,15),(12,15)]}
        r=classify_space_relations(spaces,boundaries)
        self.assertEqual(r[0]["type"],"OVERLAPS")
        self.assertEqual(r[0]["status"],"UNKNOWN")

if __name__ == "__main__": unittest.main()
