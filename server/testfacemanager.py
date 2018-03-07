import unittest
from facemanager import FaceManager
import numpy as np
import time


class TestFaceManager(unittest.TestCase):
    test_face_rep = np.array([-0.01087925,  0.06281514,  0.06941294, -0.04114388,  0.06661014,
        0.05149819,  0.05432247, -0.00484836, -0.01681362, -0.01613554,
        0.03095078, -0.07453853,  0.00809483,  0.14485705,  0.18424363,
       -0.07458271,  0.00876596, -0.08338758,  0.02281007,  0.04389508,
       -0.03684004, -0.04064358,  0.04305072, -0.02364777,  0.05940493,
       -0.04784972, -0.04001505,  0.07607707,  0.07883453, -0.07592109,
        0.09340405, -0.05863626,  0.05145449,  0.04129188,  0.06525925,
        0.17336334,  0.06649707,  0.08566447, -0.08207326, -0.13486637,
        0.07696605, -0.00889065,  0.06050812,  0.01069656, -0.14179407,
        0.10559254,  0.01925564,  0.09619909, -0.05783697,  0.00919303,
       -0.20344487,  0.03126547, -0.03591568, -0.01600742,  0.15409145,
        0.03580477, -0.18024218,  0.10426354, -0.08708039, -0.0381988,
       -0.18289317, -0.00201593,  0.10514525, -0.11796998,  0.1284215,
        0.22469789, -0.03947631,  0.02150401, -0.11290143,  0.11836369,
        0.03786717,  0.04378672, -0.02327077,  0.01201258,  0.11775552,
       -0.01940966,  0.05034143,  0.02630954,  0.09603818, -0.09977916,
       -0.02912212, -0.04142572, -0.02946539, -0.05678462, -0.00367304,
       -0.09017342, -0.03689631,  0.09863722,  0.063665,  0.1782265,
        0.21539743, -0.05815782,  0.01073892, -0.06692895,  0.04547476,
       -0.081388,  0.00636313,  0.0713684,  0.04252931, -0.04045114,
       -0.06673264,  0.02949119,  0.02829811, -0.16744904, -0.12841879,
        0.1941781,  0.01014664, -0.03339468,  0.17807868, -0.07741927,
        0.02729446,  0.0743317, -0.04170747,  0.03516954,  0.15208071,
       -0.03791773,  0.10245349, -0.05754362,  0.07515993,  0.14803457,
        0.08236565, -0.07617516,  0.02546349,  0.15618236, -0.01244762,
        0.03848226,  0.19635513,  0.01439738])

    t = time.time()
    fm = FaceManager(False)


    def test_room_starts_empty(self):
        self.assertTrue(len(self.fm.faces_in_room) == 0)


    def test_can_add_face_to_room(self):
        test_array = [self.test_face_rep, self.t, 0, None]
        self.fm.add_face_to_room(test_array)
        self.assertTrue(len(self.fm.faces_in_room) == 1)


    def test_can_remove_face_from_room(self):
        exit_array = [self.test_face_rep, time.time(), 0, None]
        self.fm.remove_face_from_room(exit_array)
        self.assertTrue(len(self.fm.faces_in_room) == 0)


    def test_can_count_faces_in_room(self):
        test_array = [self.test_face_rep, self.t, 0, None]
        self.fm.add_face_to_room(test_array)
        self.assertTrue(self.fm.get_num_faces() == 1)

    fm.process.terminate()



if __name__ == '__main__':
    unittest.main()