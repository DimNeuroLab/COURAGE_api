from flask import Blueprint, jsonify, request, json
from courage_algorithms.image_algorithms.face2bmi import predict_bmi_by_image, get_bmi_label
from courage_algorithms.image_algorithms.object_detection import object_detection_algorithm
from courage_algorithms.image_algorithms.gender_detection import predict_gender_by_image
from courage_algorithms.IT_text_algorithms.emotion_IT import predict_emotion_it
from courage_algorithms.IT_text_algorithms.sentiment_IT import predict_sentiment_it
from courage_algorithms.EN_text_algorithms.sentiment_EN import predict_sentiment_en
from courage_algorithms.EN_text_algorithms.hate_speech_detection_EN_SemEval19 import predict_hate_speech_en_semeval19
from courage_algorithms.ES_text_algorithms.sentiment_ES import predict_sentiment_es
from courage_algorithms.DE_text_algorithms.sentiment_DE import predict_sentiment_de
from courage_algorithms.EN_text_algorithms.emotion_EN import predict_emotion_en
from courage_algorithms.ES_text_algorithms.emotion_ES import predict_emotion_es
from courage_algorithms.DE_text_algorithms.toxicity_DE import get_ensemble_prediction_toxic_de
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np


# REST-Api
api_blueprint = Blueprint("api", __name__)

################################################################################################################
# GENERAL
################################################################################################################


@api_blueprint.route("info/", methods=["GET"])
def get_api_info():
    """
    Return information about the api and the server.
    """
    res = {"COURAGE": "api", "version": "1.0"}
    return jsonify(res)


################################################################################################################
# IMAGES
################################################################################################################


@api_blueprint.route("predict_bmi/", methods=["POST"])
def predict_bmi():
    """
    Predict BMI based on user image.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        predicted_bmi = float(predict_bmi_by_image(image))
        output = json.dumps({'bmi': predicted_bmi,
                             'label': get_bmi_label(predicted_bmi)})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("predict_gender/", methods=["POST"])
def predict_gender():
    """
    Predict gender based on user image.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        predicted_gender = predict_gender_by_image(image)
        output = json.dumps({'gender': predicted_gender})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("detect_objects/", methods=["POST"])
def detect_objects():
    """
    Detect objects in images using YOLOv3.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        detected_objects = object_detection_algorithm(image)
        output = json.dumps(detected_objects)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


################################################################################################################
# TEXT
################################################################################################################


###########################
# # # # # ENGLISH # # # # #
###########################


@api_blueprint.route("EN/sentiment/", methods=["POST"])
def predict_sentiment_english():
    """
    Predict Sentiment of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_en(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("EN/hate_speech_semeval19/", methods=["POST"])
def predict_hate_speech_english_semeval19():
    """
    Predict Hate Speech Characteristics of an English Text (Trained on SemEval19 dataset).
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        hateful, targeted, aggressive = predict_hate_speech_en_semeval19(text)
        output = json.dumps({'hateful': hateful,
                             'targeted': targeted,
                             'aggressive': aggressive})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("EN/emotion/", methods=["POST"])
def predict_emotion_english():
    """
    Predict Emotion of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        label, confidence = predict_emotion_en(text)
        output = json.dumps({'label': label,
                             'confidence': confidence})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


###########################
# # # # # ITALIAN # # # # #
###########################


@api_blueprint.route("IT/sentiment/", methods=["POST"])
def predict_sentiment_italian():
    """
    Predict Sentiment of an Italian Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, pos = predict_sentiment_it(text)
        output = json.dumps({'negative': neg,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("IT/emotion/", methods=["POST"])
def predict_emotion_italian():
    """
    Predict Emotion of an Italian Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        label, confidence = predict_emotion_it(text)
        output = json.dumps({'label': label,
                             'confidence': confidence})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


###########################
# # # # # SPANISH # # # # #
###########################


@api_blueprint.route("ES/sentiment/", methods=["POST"])
def predict_sentiment_spanish():
    """
    Predict Sentiment of a Spanish Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_es(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("ES/emotion/", methods=["POST"])
def predict_emotion_spanish():
    """
    Predict Emotion of a Spanish Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        label, confidence = predict_emotion_es(text)
        output = json.dumps({'label': label,
                             'confidence': confidence})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


##########################
# # # # # GERMAN # # # # #
##########################


@api_blueprint.route("DE/sentiment/", methods=["POST"])
def predict_sentiment_german():
    """
    Predict Sentiment of a German Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_de(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("DE/toxic/", methods=["POST"])
def predict_toxicity_german():
    """
    Predict whether a German Text is toxic or not.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        label = get_ensemble_prediction_toxic_de(text)
        if label == 0:
            output = json.dumps({'0': 'not toxic'})
        else:
            output = json.dumps({'1': 'toxic'})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code
