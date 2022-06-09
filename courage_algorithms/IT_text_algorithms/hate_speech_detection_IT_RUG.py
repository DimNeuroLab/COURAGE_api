import re
from nltk.corpus import stopwords
import pickle
from sklearn.base import TransformerMixin
from courage_algorithms.scripts.path_setup import get_working_dir


class Embeddings(TransformerMixin):
    def __init__(self, word_embeds, pool='max'):
        self.word_embeds = word_embeds
        self.pool_method = pool

    def transform(self, X, **transform_params):
        return [self.get_sent_embedding(sent, self.word_embeds, self.pool_method) for sent in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_sent_embedding(self, sentence, word_embeds, pool):
        l_vector = len(word_embeds['e'])
        list_of_embeddings = [word_embeds[word.lower()] for word in sentence.split() if word.lower() in word_embeds]
        if pool == 'pool':
            sent_embedding = [sum(col) / float(len(col)) for col in zip(*list_of_embeddings)]  # average pooling
        elif pool == 'max':
            sent_embedding = [max(col) for col in zip(*list_of_embeddings)]	# max pooling
        else:
            raise ValueError('Unknown pooling method!')
        if len(sent_embedding) != l_vector:
            sent_embedding = [0] * l_vector
        return sent_embedding


def preprocess_text(raw_text):
    pattern = re.compile(r'\b(' + r'|'.join(
        stopwords.words('italian')) + r')\b\s*')
    raw_text = re.sub(r'\|LBR\|', '', raw_text)
    raw_text = re.sub(r",", " , ", raw_text)
    raw_text = re.sub(r"!", " ! ", raw_text)
    raw_text = re.sub(r"\(", " \( ", raw_text)
    raw_text = re.sub(r"\)", " \) ", raw_text)
    raw_text = re.sub(r"\s{2,}", " ", raw_text)
    raw_text = re.sub(r"'", " ' ", raw_text)
    raw_text = pattern.sub('', raw_text)
    raw_text = raw_text.strip().lower()
    return raw_text


def load_pipeline():
    pipeline_path = get_working_dir() + '/courage_algorithms/models/hate_twitter_italian/evalita20_rug_tweeter_taskB.pkl'
    with open(pipeline_path, 'rb') as input_file:
        return pickle.load(input_file)['classifier']


def predict_hate_speech_it(raw_text):
    raw_text = preprocess_text(raw_text)
    model_pipeline = load_pipeline()
    prediction = model_pipeline.predict([raw_text])
    if prediction[0] == '0':
        return {'not hate': 1,
                'hate': 0}
    else:
        return {'not hate': 0,
                'hate': 1}
