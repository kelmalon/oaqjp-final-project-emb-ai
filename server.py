"""
This module handles the server functionality for emotion analysis.

It processes input statements, evaluates emotional content (anger, disgust, fear, joy, sadness),
and returns the dominant emotion.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detector():
    """
    Analyze the emotional content of a given text input.

    This function retrieves a text input from the request arguments, processes it to determine
    the levels of various emotions (anger, disgust, fear, joy, sadness), and identifies the 
    dominant emotion. If the input is invalid (empty or just whitespace), it returns a default 
    response indicating no emotions detected.

    Returns:
        str: A message detailing the analyzed emotional content, including specific emotion levels
        and the dominant emotion. If the input text is invalid, returns a message prompting 
        the user to try again.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze or not text_to_analyze.strip():
        response =  {
            "emotions": {
                "anger": "None",
                "disgust": "None",
                "fear": "None",
                "joy": "None",
                "sadness": "None"
            },
            "dominant_emotion": "None",
            "dominant_score": "None"
        }
    else:
        response = emotion_detector(text_to_analyze)

    emotions = response["emotions"]

    anger = emotions['anger']
    disgust = emotions["disgust"]
    fear = emotions["fear"]
    joy = emotions["joy"]
    sadness = emotions["sadness"]

    dominant_emotion = response.get('dominant_emotion', 'None')

    if dominant_emotion == 'None':
        return "Invalid text! Please try again!"

    return {f"For the given statement, the system response is 'anger': {anger}"
    f", 'disgust': {disgust}, 'fear': {fear}, 'joy': {joy}, and 'sadness': {sadness}."
    f"The dominant emotion is {dominant_emotion}."}

@app.route("/")
def render_index_page():
    """
    Render the index page of the Emotion Detector web application.

    This function handles requests to the root URL ("/") and returns the HTML
    template for the index page. It serves as the entry point for users to 
    interact with the Emotion Detector application.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)
