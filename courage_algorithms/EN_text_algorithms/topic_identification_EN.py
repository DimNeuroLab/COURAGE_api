import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir


def load_tokenizer():
    return AutoTokenizer.from_pretrained(get_working_dir() + '/courage_algorithms/models/BERT_topic_identification',
                                         local_files_only=True)


def load_model():
    return AutoModelForSequenceClassification.from_pretrained(get_working_dir() + '/courage_algorithms/models/BERT_topic_identification',
                                                              local_files_only=True)


def predict_topic_en(sentence, tokenizer=None, model=None):
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if model is None:
        model = load_model()

    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)

    outputs = model(**inputs)
    logits = outputs['logits']
    logits = logits.squeeze(0)

    proba = torch.sigmoid(logits)
    proba = np.array(proba.detach().numpy())

    label_names = ['arts_&_culture', 'business_&_entrepreneurs', 'celebrity_&_pop_culture', 'diaries_&_daily_life',
                   'family', 'fashion_&_style', 'film_tv_&_video', 'fitness_&_health', 'food_&_dining', 'gaming',
                   'learning_&_educational', 'music', 'news_&_social_concern', 'other_hobbies', 'relationships',
                   'science_&_technology', 'sports', 'travel_&_adventure', 'youth_&_student_life']
    ranking = np.argsort(proba)
    ranking = ranking[::-1]
    output = {}
    for i in range(proba.shape[0]):
        output[label_names[ranking[i]]] = np.round(float(proba[ranking[i]]), 4)
    return output


def load_cip_tokenizer():
    return AutoTokenizer.from_pretrained(
        get_working_dir() + '/courage_algorithms/models/standard_models/bert-base-cased',
        local_files_only=True)


def load_cip_model():
    return AutoModelForSequenceClassification.from_pretrained(
        get_working_dir() + '/courage_algorithms/models/BERT_topic_multi',
        local_files_only=True)


def predict_cip_topic(sentence, tokenizer=None, model=None):
    if tokenizer is None:
        tokenizer = load_tokenizer()
    if model is None:
        model = load_cip_model()

    inputs = tokenizer(sentence, return_tensors="pt")

    labels = torch.tensor([1]).unsqueeze(0)
    outputs = model(**inputs, labels=labels)
    loss, logits = outputs[:2]
    logits = logits.squeeze(0)

    proba = torch.softmax(logits, dim=0)
    other, covid, immigrants, politics = proba

    return {'other': np.round(other.item(), 4), 'covid': np.round(covid.item(), 4),
            'immigrants': np.round(immigrants.item(), 4), 'politics': np.round(politics.item(), 4)}
