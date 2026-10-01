import unittest
from runtime.space_extraction import polygonize_orthogonal_lines

class SpaceExtractionTests(unittest.TestCase):
    def test_four_walls_form_one_space(self):
        lines=[
            (0,0,10,0,"a"),(10,0,10,10,"b"),(10,10,0,10,"c"),(0,10,0,0,"d")
        ]
        faces=polygonize_orthogonal_lines(lines)
        self.assertEqual(len(faces),1)
        self.assertAlmostEqual(faces[0][1],100.0)

    def test_two_adjacent_spaces_are_extracted_separately(self):
        lines=[
            (0,0,20,0,"a"),(20,0,20,10,"b"),(20,10,0,10,"c"),(0,10,0,0,"d"),
            (10,0,10,10,"e")
        ]
        faces=polygonize_orthogonal_lines(lines)
        areas=sorted(round(a,6) for _,a in faces)
        self.assertEqual(areas,[100.0,100.0])

    def test_diagonal_lines_are_not_promoted_to_spaces(self):
        self.assertEqual(polygonize_orthogonal_lines([(0,0,10,10,"x")]),[])

if __name__=="__main__": unittest.main()
