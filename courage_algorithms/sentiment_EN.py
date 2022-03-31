import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis",
                                         cache_dir=get_working_dir() + '/courage_algorithms/models/Bertweet_sentiment_EN')


def load_model():
    return AutoModelForSequenceClassification.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis",
                                                              cache_dir=get_working_dir() + '/courage_algorithms/models/Bertweet_sentiment_EN')


def predict_sentiment_en(sentence):
    tokenizer = load_tokenizer()
    model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    labels = torch.tensor([1]).unsqueeze(0)
    outputs = model(**inputs, labels=labels)
    loss, logits = outputs[:2]
    logits = logits.squeeze(0)
    proba = torch.softmax(logits, dim=0)
    negative, neutral, positive = proba

    return np.round(negative.item(), 4), np.round(neutral.item(), 4), np.round(positive.item(), 4)
