import unittest

class TestSpeakerClient(unittest.TestCase):
    
    def test_seconds_correctly_to_string():
        test_1 = 4        
        test_2 = 137        
        test_3 = 4386        
        test_4 = 120        
        test_5 = 7260
        
        answer_1 = "4 seconds "
        answer_2 = "2 minutes 17 seconds"
        answer_3 = "1 hour 13 minutes 6 seconds"
        answer_4 = "2 minutes "
        answer_5 = "2 hours 1 minutes"

        unittest.assertEqual(
            speaker_client.seconds_to_string(test_1),
            answer_1)

        unittest.assertEqual(
            speaker_client.seconds_to_string(test_2),
            answer_2)
            
        unittest.assertEqual(
            speaker_client.seconds_to_string(test_3),
            answer_3)

        unittest.assertEqual(
            speaker_client.seconds_to_string(test_4),
            answer_4)

        unittest.assertEqual(
            speaker_client.seconds_to_string(test_5),
            answer_5)

    def test_should_say():
        curr_time = time.time()
        long_time_ago = curr_time - 20

        unittest.assertTrue(
            speaker_client.should_say(long_time_ago) )

        unittest.assertFalse(
            speaker_client.should_say(curr_time) )



