import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-emotion",
                                         cache_dir=get_working_dir() + '/courage_algorithms/models/MilaNLP_emotion')


def load_model():
    return AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-emotion",
                                                              cache_dir=get_working_dir() + '/courage_algorithms/models/MilaNLP_emotion')


def predict_emotion_it(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    labels = torch.tensor([1]).unsqueeze(0)
    outputs = model(**inputs, labels=labels)
    loss, logits = outputs[:2]
    logits = logits.squeeze(0)

    proba = torch.softmax(logits, dim=0)
    proba = np.array(proba.detach().numpy())

    label_names = ['anger', 'fear', 'joy', 'sadness']
    ranking = np.argsort(proba)
    ranking = ranking[::-1]
    for i in range(proba.shape[0]):
        l = label_names[ranking[i]]
        s = proba[ranking[i]]
        return l, np.round(float(s), 4)
