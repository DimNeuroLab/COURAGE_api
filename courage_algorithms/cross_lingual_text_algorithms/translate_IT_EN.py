from transformers import pipeline
from courage_algorithms.scripts.path_setup import get_working_dir


def load_translator():
    translator = pipeline("translation",
                          model=get_working_dir() + '/courage_algorithms/models/translate_IT_EN')
    return translator


def translate_it_en(sentence):
    translator = load_translator()
    translation = translator(sentence)
    return translation[0]
