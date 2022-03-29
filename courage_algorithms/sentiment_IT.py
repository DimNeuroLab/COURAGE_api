import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-sentiment",
                                         cache_dir=get_working_dir() + '/courage_algorithms/models/MilaNLP_sentiment')


def load_model():
    return AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-sentiment",
                                                              cache_dir=get_working_dir() + '/courage_algorithms/models/MilaNLP_sentiment')


def predict_sentiment_it(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    labels = torch.tensor([1]).unsqueeze(0)
    outputs = model(**inputs, labels=labels)
    loss, logits = outputs[:2]
    logits = logits.squeeze(0)

    proba = torch.nn.functional.softmax(logits, dim=0)
    negative, positive = proba

    return np.round(negative.item(), 4), np.round(positive.item(), 4)
