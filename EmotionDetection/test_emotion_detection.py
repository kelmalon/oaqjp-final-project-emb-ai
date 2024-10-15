import sys
import os

from emotion_detection import emotion_detector
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestEmotionDetector(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        # Propagate exceptions to the test client
        app.testing = True
    
    def test_emotion_detector(self):
        result1 = emotion_detector('I am glad this happened')
        self.assertEqual(result1['dominant_emotion'], 'joy')

        result2 = emotion_detector('I am really mad about this')
        self.assertEqual(result2['dominant_emotion'], 'anger')

        result3 = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result3['dominant_emotion'], 'disgust')

        result4 = emotion_detector('I am so sad about this')
        self.assertEqual(result4['dominant_emotion'], 'sadness')

        result5 = emotion_detector('I am really afraid that this will happen')
        self.assertEqual(result5['dominant_emotion'], 'fear')

    def test_missing_textToAnalyze(self):
        # Send a GET request without the 'textToAnalyze' argument
        response = self.client.get('/emotionDetector')  # Use the test client to call the route

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Optionally check the error message in the response data
        self.assertIn(b"Error: No text provided for analysis", response.data)

unittest.main()

