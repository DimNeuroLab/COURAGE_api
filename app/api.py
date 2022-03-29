from flask import Blueprint, jsonify, request, json
from courage_algorithms.face2bmi import *
from courage_algorithms.object_detection import *
from courage_algorithms.gender_detection import *
from courage_algorithms.emotion_IT import *
from courage_algorithms.sentiment_IT import *
import json
import base64
from io import BytesIO
from PIL import Image


# REST-Api
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("info/", methods=["GET"])
def get_api_info():
    """
    Return information about the api and the server.
    """
    res = {"COURAGE": "api", "version": "1.0"}
    return jsonify(res)


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


@api_blueprint.route("sentiment_IT/", methods=["POST"])
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


@api_blueprint.route("emotion_IT/", methods=["POST"])
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
