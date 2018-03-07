import unittest
from facerecognitionjob import FaceRecognitionJob
from multiprocessing import Queue, Process
import time

def busy_fake_classifier(x):
    time.sleep(0.25)
    return x

class TestFaceRecognitionJob(unittest.TestCase):
    image = 0
    t = 0
    door = 0

    def test_produces_output(self):
        q = Queue()
        self.assertTrue(q.empty())
        FaceRecognitionJob(self.image, self.t, self.door, q, lambda x: x).run()
        time.sleep(0.01)
        self.assertFalse(q.empty())

    def test_timestamp_preserved(self):
        my_time = 5432
        q = Queue()
        FaceRecognitionJob(self.image, my_time, self.door, q, lambda x: x).run()
        their_time = q.get()[1]
        self.assertEqual(my_time, their_time)

    def test_door_preserved(self):
        my_door = 4
        q = Queue()
        FaceRecognitionJob(self.image, self.t, my_door, q, lambda x: x).run()
        their_door = q.get()[2]
        self.assertEqual(my_door, their_door)        
     
    def test_can_operate_in_another_thread(self):
        q = Queue()
        job = FaceRecognitionJob(self.image, self.t, self.door, q, busy_fake_classifier)
        p = Process(target = job.run)
        p.start()
        self.assertTrue(q.empty())
        time.sleep(0.5)
        self.assertFalse(q.empty())

if __name__ == '__main__':
    unittest.main()
