import os
from flask import Blueprint, jsonify, request, json
from courage_algorithms.image_algorithms.face2bmi import predict_bmi_by_image, get_bmi_label
from courage_algorithms.image_algorithms.object_detection import object_detection_algorithm
from courage_algorithms.image_algorithms.gender_detection import predict_gender_by_image
from courage_algorithms.IT_text_algorithms.emotion_IT import predict_emotion_it
from courage_algorithms.IT_text_algorithms.sentiment_IT import predict_sentiment_it
from courage_algorithms.EN_text_algorithms.sentiment_EN import predict_sentiment_en
from courage_algorithms.EN_text_algorithms.hate_speech_detection_EN_SemEval19 import predict_hate_speech_en_semeval19
from courage_algorithms.ES_text_algorithms.sentiment_ES import predict_sentiment_es
from courage_algorithms.DE_text_algorithms.sentiment_DE import predict_sentiment_de
from courage_algorithms.EN_text_algorithms.emotion_EN import predict_emotion_en
from courage_algorithms.ES_text_algorithms.emotion_ES import predict_emotion_es
from courage_algorithms.DE_text_algorithms.toxicity_DE import get_ensemble_prediction_toxic_de
from courage_algorithms.IT_text_algorithms.hate_speech_detection_IT_RUG import predict_hate_speech_it
from crawler import *
from courage_algorithms.scripts.path_setup import get_working_dir
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import time


# REST-Api
api_blueprint = Blueprint("api", __name__)

################################################################################################################
# GENERAL
################################################################################################################


@api_blueprint.route("info/", methods=["GET"])
def get_api_info():
    """
    Return information about the api and the server.
    """
    res = {"COURAGE": "api", "version": "1.0"}
    return jsonify(res)


################################################################################################################
# TWITTER DEMO
################################################################################################################


@api_blueprint.route("load_twitter_data/", methods=["GET"])
def load_twitter_data():
    """
    Load tweets to serve demo page.
    """
    tweets = []
    try:
        for file in os.listdir(get_working_dir() + '/app/webapp/tweets'):
            if file.endswith('json'):
                file_data = []
                with open(get_working_dir() + '/app/webapp/tweets/' + file) as json_file:
                    file_data.append(json.load(json_file))
                with open(get_working_dir() + '/app/webapp/analysis_results/' + file) as json_file:
                    file_data.append(json.load(json_file))
                tweets.append(file_data)
        status_code = 200
    except:
        status_code = 444
    res = {"tweets": tweets}
    return jsonify(res), status_code


@api_blueprint.route("load_tweets_user/", methods=["POST"])
def load_tweets_user():
    """
    Load timeline tweets of a specific user.
    """
    data = request.json
    if 'user_id' in data:
        user_id = data['user_id']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        folder_path = get_working_dir() + '/app/webapp/tweets_users/' + user_id
        tweet_list = []
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('json'):
                    with open(folder_path + '/' + file) as json_file:
                        tweet_list.append(json.load(json_file))
        status_code = 200
        res = {"tweets": tweet_list}
    except:
        status_code = 444
        res = {"tweets": []}
    return res, status_code


@api_blueprint.route("load_tweets_topic/", methods=["POST"])
def load_tweets_topic():
    """
    Load tweets related to a specific topic.
    """
    data = request.json
    if 'topic' in data:
        topic = data['topic']
    else:
        # no text posted
        status_code = 400
        return status_code
    if 'n' in data:
        num_tweets = data['n']
    else:
        num_tweets = None
    try:
        folder_path = get_working_dir() + '/app/webapp/tweets_topics/' + topic
        tweet_list = []
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('json'):
                    with open(folder_path + '/' + file) as json_file:
                        tweet_list.append(json.load(json_file))
        status_code = 200
        if num_tweets:
            res = {"tweets": tweet_list[:num_tweets]}
        else:
            res = {"tweets": tweet_list}
    except:
        status_code = 444
        res = {"tweets": []}
    return res, status_code


@api_blueprint.route("analyze_twitter_data/", methods=["GET"])
def analyze_twitter_data():
    """
    Run analysis algorithms on available tweets.
    """
    try:
        for file in os.listdir(get_working_dir() + '/app/webapp/tweets'):
            analysis_results = {}
            if file.endswith('json'):
                print('processing file...', file)

                with open(get_working_dir() + '/app/webapp/tweets/' + file) as json_file:
                    tweet_text = json.load(json_file)['text']

                neg, neu, pos = predict_sentiment_en(tweet_text)
                analysis_results['sentiment'] = {'negative': neg, 'neutral': neu, 'positive': pos}

                analysis_results['emotion'] = predict_emotion_en(tweet_text)

                hateful, targeted, aggressive = predict_hate_speech_en_semeval19(tweet_text)
                analysis_results['hate_speech'] = {'hateful': hateful, 'targeted': targeted, 'aggressive': aggressive}

                with open(get_working_dir() + '/app/webapp/analysis_results/' + file, 'w') as json_file:
                    json.dump(analysis_results, json_file)

        for folder in os.listdir(get_working_dir() + '/app/webapp/tweets_users'):
            user_sentiment = {'negative': [], 'neutral': [], 'positive': []}
            user_emotion = {'sadness': [], 'anger': [], 'joy': [], 'optimism': []}
            for file in os.listdir(get_working_dir() + '/app/webapp/tweets_users/' + folder)[:10]:
                if file.endswith('json'):
                    print('processing user + file...', folder, file)

                    with open(get_working_dir() + '/app/webapp/tweets_users/' + folder + '/' + file) as json_file:
                        tweet_text = json.load(json_file)['text']

                    neg, neu, pos = predict_sentiment_en(tweet_text)
                    user_sentiment['negative'].append(neg)
                    user_sentiment['neutral'].append(neu)
                    user_sentiment['positive'].append(pos)

                    emotion_results = predict_emotion_en(tweet_text)
                    user_emotion['sadness'].append(emotion_results['sadness'])
                    user_emotion['anger'].append(emotion_results['anger'])
                    user_emotion['joy'].append(emotion_results['joy'])
                    user_emotion['optimism'].append(emotion_results['optimism'])

            user_sentiment = {key: sum(value) / len(value) for key, value in user_sentiment.items()}
            user_emotion = {key: sum(value) / len(value) for key, value in user_emotion.items()}
            analysis_results = {'sentiment': {}, 'emotion': {}}
            sum_all_sentiment = sum([user_sentiment['negative'], user_sentiment['neutral'], user_sentiment['positive']])
            analysis_results['sentiment']['negative'] = user_sentiment['negative'] / sum_all_sentiment
            analysis_results['sentiment']['neutral'] = user_sentiment['neutral'] / sum_all_sentiment
            analysis_results['sentiment']['positive'] = user_sentiment['positive'] / sum_all_sentiment
            sum_all_emotion = sum([user_emotion['sadness'], user_emotion['anger'], user_emotion['joy'], user_emotion['optimism']])
            analysis_results['emotion']['sadness'] = user_emotion['sadness'] / sum_all_emotion
            analysis_results['emotion']['anger'] = user_emotion['anger'] / sum_all_emotion
            analysis_results['emotion']['joy'] = user_emotion['joy'] / sum_all_emotion
            analysis_results['emotion']['optimism'] = user_emotion['optimism'] / sum_all_emotion

            with open(get_working_dir() + '/app/webapp/analysis_results/tweets_users/' + folder + '.json', 'w') as json_file:
                json.dump(analysis_results, json_file)
        status_code = 200
    except:
        status_code = 444
    res = {"status": 'SUCCESSFUL'}
    return jsonify(res), status_code


@api_blueprint.route("crawl_new_data/", methods=["GET"])
def crawl_new_data():
    """
    Crawl new data for feed.
    """
    try:
        stream = initialize_stream()
        stream_stats = {'users': 0,
                        'topics': 0}

        delete_home_timeline_dir()

        home_tweets = get_home_timeline_tweets(stream)
        users = []
        topics = []
        for tweet in home_tweets:
            topics += get_tweet_topic(tweet)
            users.append(tweet['user']['id_str'])
            save_home_tweet(tweet)

        topics = list(set(topics))
        for topic in topics:
            # if stream_stats['topics'] * 15 >= 450:
            #    print('sleeping for 15min to get new topics...')
            #    time.sleep(901)
            create_new_topic_folder(topic)
            delete_topic_tweet_dir(topic)
            topic_tweets = search_tweets(stream, topic)
            for topic_tweet in topic_tweets:
                save_topic_tweet(topic_tweet, topic)
            stream_stats['topics'] += 1

        for user_id in users:
            create_new_user_folder(user_id)
            delete_user_tweet_dir(user_id)
            user_tweets = get_user_timeline_tweets(stream, user_id)
            for user_tweet in user_tweets:
                save_user_tweet(user_tweet, user_id)
            stream_stats['users'] += 1
                
        status_code = 200
    except:
        status_code = 444
    res = {"status": 'SUCCESSFUL'}
    return jsonify(res), status_code


@api_blueprint.route("load_algorithm_results/", methods=["POST"])
def load_algorithm_data():
    """
    Get prediction examples of a specific algorithm.
    """
    data = request.json
    if 'file_name' in data:
        file_name = data['file_name']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        file_path = get_working_dir() + '/app/webapp/algorithms_predictions/' + file_name
        file_content = []
        with open(file_path, 'r') as algo_file:
            for line in algo_file:
                line = line.strip('\n').split('\t')
                file_content.append(line)
        output = json.dumps({'predictions': file_content})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("load_user_tweets_analysis/", methods=["POST"])
def load_user_tweets_analysis():
    """
    Get analysis results of a user's tweets.
    """
    data = request.json
    if 'user_id' in data:
        user_id = data['user_id']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        file_path = get_working_dir() + '/app/webapp/analysis_results/tweets_users/' + user_id + '.json'
        with open(file_path) as json_file:
            analysis_results = json.load(json_file)
        status_code = 200
    except:
        # error
        analysis_results = {}
        status_code = 444
    return jsonify(analysis_results), status_code


################################################################################################################
# IMAGES
################################################################################################################


@api_blueprint.route("predict_bmi/", methods=["POST"])
def predict_bmi():
    """
    Predict BMI based on user image.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        predicted_bmi = float(predict_bmi_by_image(image))
        output = json.dumps({'bmi': predicted_bmi,
                             'label': get_bmi_label(predicted_bmi)})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("predict_gender/", methods=["POST"])
def predict_gender():
    """
    Predict gender based on user image.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        predicted_gender = predict_gender_by_image(image)
        output = json.dumps({'gender': predicted_gender})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("detect_objects/", methods=["POST"])
def detect_objects():
    """
    Detect objects in images using YOLOv3.
    """
    data = request.json
    if 'image' in data:
        image = data['image']
        image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
    else:
        # no image posted
        status_code = 400
        return status_code
    try:
        detected_objects = object_detection_algorithm(image)
        output = json.dumps(detected_objects)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


################################################################################################################
# TEXT
################################################################################################################


###########################
# # # # # ENGLISH # # # # #
###########################


@api_blueprint.route("EN/sentiment/", methods=["POST"])
def predict_sentiment_english():
    """
    Predict Sentiment of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_en(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("EN/hate_speech_semeval19/", methods=["POST"])
def predict_hate_speech_english_semeval19():
    """
    Predict Hate Speech Characteristics of an English Text (Trained on SemEval19 dataset).
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        hateful, targeted, aggressive = predict_hate_speech_en_semeval19(text)
        output = json.dumps({'hateful': hateful,
                             'targeted': targeted,
                             'aggressive': aggressive})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("EN/emotion/", methods=["POST"])
def predict_emotion_english():
    """
    Predict Emotion of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        emotion_dict = predict_emotion_en(text)
        output = json.dumps(emotion_dict)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


###########################
# # # # # ITALIAN # # # # #
###########################


@api_blueprint.route("IT/sentiment/", methods=["POST"])
def predict_sentiment_italian():
    """
    Predict Sentiment of an Italian Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, pos = predict_sentiment_it(text)
        output = json.dumps({'negative': neg,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("IT/emotion/", methods=["POST"])
def predict_emotion_italian():
    """
    Predict Emotion of an Italian Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        emotion_dict = predict_emotion_it(text)
        output = json.dumps(emotion_dict)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("IT/hate_speech/", methods=["POST"])
def predict_hate_speech_italian():
    """
    Predict whether an Italian Text is hate speech or not.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        hate_speech_it = predict_hate_speech_it(text)
        output = json.dumps(hate_speech_it)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


###########################
# # # # # SPANISH # # # # #
###########################


@api_blueprint.route("ES/sentiment/", methods=["POST"])
def predict_sentiment_spanish():
    """
    Predict Sentiment of a Spanish Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_es(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("ES/emotion/", methods=["POST"])
def predict_emotion_spanish():
    """
    Predict Emotion of a Spanish Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        emotion_dict = predict_emotion_es(text)
        output = json.dumps(emotion_dict)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


##########################
# # # # # GERMAN # # # # #
##########################


@api_blueprint.route("DE/sentiment/", methods=["POST"])
def predict_sentiment_german():
    """
    Predict Sentiment of a German Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        neg, neu, pos = predict_sentiment_de(text)
        output = json.dumps({'negative': neg,
                             'neutral': neu,
                             'positive': pos})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("DE/toxic/", methods=["POST"])
def predict_toxicity_german():
    """
    Predict whether a German Text is toxic or not.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        toxic_de = get_ensemble_prediction_toxic_de(text)
        output = json.dumps(toxic_de)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code
