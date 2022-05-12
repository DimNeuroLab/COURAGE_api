import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/RoBERTuito_emotion_ES',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/RoBERTuito_emotion_ES',
                                                              local_files_only=True)


def predict_emotion_es(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs['logits']
    logits = logits.squeeze(0)

    proba = torch.softmax(logits, dim=0)
    proba = np.array(proba.detach().numpy())

    label_names = ['others', 'joy', 'sadness', 'anger', 'surprise', 'disgust', 'fear']
    ranking = np.argsort(proba)
    ranking = ranking[::-1]
    for i in range(proba.shape[0]):
        l = label_names[ranking[i]]
        s = proba[ranking[i]]
        return l, np.round(float(s), 4)
