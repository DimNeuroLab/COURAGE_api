import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
import tensorflow as tf
from path_setup import get_working_dir


def crop_img(image, x, y, w, h):
    return image[y:(y+h), x:(x+w), :]


def detect_face(image):
    face_detector = MTCNN()
    box = face_detector.detect_faces(image)[0]
    return box


def get_bmi_label(y):
    if y < 18.5:
        return 'Underweight'
    elif y < 25:
        return 'NormalWeight'
    elif y < 30:
        return 'Overweight'
    elif y < 35:
        return 'Obese'
    elif y < 40:
        return 'SeverelyObese'
    else: # y >= 40:
        return 'MorbidlyObese'


def load_model():
    custom_vgg_model = tf.keras.models.load_model(get_working_dir() + '/courage_algorithms/models/bmi_detector/bmi_detector.h5')
    return custom_vgg_model


def predict_bmi_by_image(image):
    image = crop_img(image, *detect_face(image)['box'])
    image = cv2.resize(image, (224, 224))
    image = image/255.0
    model = load_model()
    return model.predict(image[np.newaxis, :, :, :])[0][0]
