import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/Bertweet_sentiment_EN',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/Bertweet_sentiment_EN',
                                                              local_files_only=True)


def predict_sentiment_en(sentence, tokenizer=None, model=None):
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if model is None:
        model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=128)

    labels = torch.tensor([1]).unsqueeze(0)
    outputs = model(**inputs, labels=labels)
    loss, logits = outputs[:2]
    logits = logits.squeeze(0)
    proba = torch.softmax(logits, dim=0)
    negative, neutral, positive = proba

    return np.round(negative.item(), 4), np.round(neutral.item(), 4), np.round(positive.item(), 4)
