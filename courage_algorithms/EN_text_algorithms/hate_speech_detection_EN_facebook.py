import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/RoBERTa_hate_speech_EN',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/RoBERTa_hate_speech_EN',
                                                              local_files_only=True)


def predict_hate_speech_en_facebook(sentence, tokenizer=None, model=None):
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if model is None:
        model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs[0]
    logits = logits.squeeze(0)

    proba = torch.softmax(logits, dim=0)
    not_hate, hate = proba

    return np.round(not_hate.item(), 4), np.round(hate.item(), 4)
