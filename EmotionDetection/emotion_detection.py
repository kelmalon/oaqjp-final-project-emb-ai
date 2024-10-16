import requests, json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(url, json = myobj, headers = headers)
    status_code = response.status_code
    
    if not text_to_analyze.strip() or text_to_analyze == "None":
        return {
            "error": "Bad request - No text provided or improperly formatted",
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

    match status_code:
        case 200:
            emotions_data = response.json()

            emotions = emotions_data['emotionPredictions'][0]['emotion']

            required_emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
            extracted_emotions = {emotion: emotions.get(emotion, 0) for emotion in required_emotions}

            if all(score == 0 for score in emotions.values()):
                dominant_emotion = 'none'
                dominant_score = 0
            else:
                dominant_emotion = max(emotions, key=emotions.get)
                dominant_score = emotions[dominant_emotion]

            result = {
                "emotions": emotions, 
                "dominant_emotion": dominant_emotion,
                "dominant_score": dominant_score
            }

            return result
        case 400:
            result = {
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
        case _:
            return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

