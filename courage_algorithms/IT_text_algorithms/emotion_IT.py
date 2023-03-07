import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/MilaNLP_emotion',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/MilaNLP_emotion',
                                                              local_files_only=True)


def predict_emotion_it(sentence, tokenizer=None, model=None):
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if model is None:
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
    output = {}
    for i in range(proba.shape[0]):
        output[label_names[ranking[i]]] = np.round(float(proba[ranking[i]]), 4)
    return output
