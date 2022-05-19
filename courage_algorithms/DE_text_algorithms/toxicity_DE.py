from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from courage_algorithms.scripts.path_setup import get_working_dir
import torch
from flair.embeddings import TransformerDocumentEmbeddings, DocumentPoolEmbeddings, FlairEmbeddings
from flair.data import Sentence
import pickle
import numpy as np


def get_mBERT_prediction(text):
    tokenizer = AutoTokenizer.from_pretrained(get_working_dir() + "/courage_algorithms/models/standard_models/bert-base-multilingual-cased",
                                              local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(get_working_dir() + "/courage_algorithms/models/Ensemble_Toxicity_DE/mBERT")

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs['logits']
    logits = logits.squeeze(0)
    proba = torch.sigmoid(logits)
    label = torch.argmax(proba)
    return label.item()


def get_flair_XLM_embedding(text):
    transformer_embedding = TransformerDocumentEmbeddings(get_working_dir() + "/courage_algorithms/models/standard_models/xlm-roberta-base",
                                                          local_files_only=True)
    sentence = Sentence(text)
    transformer_embedding.embed(sentence)
    embedding = sentence.embedding.cpu()
    embedding = embedding.detach().numpy()
    return embedding


def get_flair_document_embedding(text):
    flair_embedding_forward = FlairEmbeddings('de-forward')
    flair_embedding_backward = FlairEmbeddings('de-backward')
    document_embeddings = DocumentPoolEmbeddings([flair_embedding_forward, flair_embedding_backward])
    sentence = Sentence(text)
    document_embeddings.embed(sentence)
    embedding = sentence.embedding.cpu()
    embedding = embedding.detach().numpy()
    return embedding


def get_model_2_prediction(embedding):
    model_2_path = get_working_dir() + "/courage_algorithms/models/Ensemble_Toxicity_DE/model_2.pickle"
    with open(model_2_path, 'rb') as handle:
        model_2 = pickle.load(handle)['model']
    return model_2.predict(np.array([embedding]))[0]


def get_model_3_prediction(embedding):
    model_3_path = get_working_dir() + "/courage_algorithms/models/Ensemble_Toxicity_DE/model_3.pickle"
    with open(model_3_path, 'rb') as handle:
        model_3 = pickle.load(handle)['model']
    return model_3.predict(np.array([embedding]))[0]


def get_ensemble_prediction_toxic_de(text):
    predictions = []
    predictions.append(get_mBERT_prediction(text))
    embedding_model_2 = get_flair_document_embedding(text)
    predictions.append(get_model_2_prediction(embedding_model_2))
    embedding_model_3 = get_flair_XLM_embedding(text)
    predictions.append(get_model_3_prediction(embedding_model_3))
    count_0 = predictions.count(0)
    count_1 = predictions.count(1)
    print(count_0, count_1)
    if count_0 > count_1:
        return {'not toxic': 1,
                'toxic': 0}
    else:
        return {'not toxic': 0,
                'toxic': 1}
