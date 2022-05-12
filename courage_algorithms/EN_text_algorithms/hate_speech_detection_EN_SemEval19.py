import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/Bertweet_hate_speech_EN',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/Bertweet_hate_speech_EN',
                                                              local_files_only=True)


def predict_hate_speech_en_semeval19(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs[0]
    logits = logits.squeeze(0)
    proba = torch.sigmoid(logits)
    hateful, targeted, aggressive = proba[0], proba[1], proba[2]

    return np.round(hateful.item(), 4), np.round(targeted.item(), 4), np.round(aggressive.item(), 4)
