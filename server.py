from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detector():
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return "Error: No text provided for analysis", 400
    
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

    return f"For the given statement, the system response is 'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, and 'sadness': {sadness}. The dominant emotion is {dominant_emotion}."

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)