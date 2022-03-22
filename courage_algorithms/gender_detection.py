from deepface import DeepFace
from mtcnn.mtcnn import MTCNN
import cv2
import numpy as np


def crop_img(image, x, y, w, h):
    return image[y:(y+h), x:(x+w), :]


def detect_face(image):
    face_detector = MTCNN()
    box = face_detector.detect_faces(image)[0]
    return box


def get_label(y):
    label_int = np.argmax(y)
    if label_int == 0:
        return 'female'
    elif label_int == 1:
        return 'male'
    else:
        return 'undefined'


def predict_gender_by_image(image):
    image = crop_img(image, *detect_face(image)['box'])
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    gender_model = DeepFace.build_model('Gender')
    prediction = gender_model.predict(image[np.newaxis, :, :, :])[0]
    return get_label(prediction)
