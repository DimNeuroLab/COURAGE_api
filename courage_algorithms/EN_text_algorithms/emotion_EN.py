import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion",
                                         cache_dir=get_working_dir() + '/courage_algorithms/models/RoBERTa_emotion_EN')


def load_model():
    return AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-emotion",
                                                              cache_dir=get_working_dir() + '/courage_algorithms/models/RoBERTa_emotion_EN')


def predict_emotion_en(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs['logits']
    logits = logits.squeeze(0)

    proba = torch.softmax(logits, dim=0)
    proba = np.array(proba.detach().numpy())

    label_names = ['joy', 'optimism', 'anger', 'sadness']
    ranking = np.argsort(proba)
    ranking = ranking[::-1]
    for i in range(proba.shape[0]):
        l = label_names[ranking[i]]
        s = proba[ranking[i]]
        return l, np.round(float(s), 4)
