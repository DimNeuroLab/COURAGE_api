import nltk
import os


def get_working_dir():
    absolute_path = os.path.abspath(os.getcwd())
    directory = []
    for cmp in absolute_path.split('/'):
        if cmp != 'COURAGE_api':
            directory.append(cmp)
        else:
            break
    return '/'.join(directory) + '/COURAGE_api'


WORKING_DIRECTORY = get_working_dir()
assert WORKING_DIRECTORY.split('/')[-1] == 'COURAGE_api'


if WORKING_DIRECTORY + '/courage_algorithms/resources/nltk' not in nltk.data.path:
    nltk.data.path.append(WORKING_DIRECTORY + '/courage_algorithms/resources/nltk')

if not os.path.exists(WORKING_DIRECTORY + '/courage_algorithms/resources/nltk/corpora'):
    nltk.download('stopwords', download_dir=WORKING_DIRECTORY + '/courage_algorithms/resources/nltk')
