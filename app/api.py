import os
from flask import Blueprint, jsonify, request, json
from courage_algorithms.image_algorithms.face2bmi import predict_bmi_by_image, get_bmi_label
from courage_algorithms.image_algorithms.object_detection import object_detection_algorithm
from courage_algorithms.image_algorithms.gender_detection import predict_gender_by_image
from courage_algorithms.IT_text_algorithms.emotion_IT import predict_emotion_it
from courage_algorithms.IT_text_algorithms.sentiment_IT import predict_sentiment_it
from courage_algorithms.EN_text_algorithms.sentiment_EN import predict_sentiment_en
from courage_algorithms.EN_text_algorithms.hate_speech_detection_EN_SemEval19 import predict_hate_speech_en_semeval19
from courage_algorithms.EN_text_algorithms.hate_speech_detection_EN_facebook import predict_hate_speech_en_facebook
from courage_algorithms.ES_text_algorithms.sentiment_ES import predict_sentiment_es
from courage_algorithms.DE_text_algorithms.sentiment_DE import predict_sentiment_de
from courage_algorithms.EN_text_algorithms.emotion_EN import predict_emotion_en
from courage_algorithms.ES_text_algorithms.emotion_ES import predict_emotion_es
from courage_algorithms.DE_text_algorithms.toxicity_DE import get_ensemble_prediction_toxic_de
from courage_algorithms.IT_text_algorithms.hate_speech_detection_IT_RUG import predict_hate_speech_it
from courage_algorithms.EN_text_algorithms.topic_identification_EN import predict_topic_en, predict_cip_topic
from courage_algorithms.cross_lingual_text_algorithms.translate_IT_EN import translate_it_en
from crawler import *
from courage_algorithms.scripts.path_setup import get_working_dir
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import random
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
    return jsonify(res), status_code


@api_blueprint.route("load_user_following_data/", methods=["POST"])
def load_user_following_data():
    """
    Load list of following ids of specific user for demo page.
    """
    data = request.json
    if 'user_id' in data:
        user_id = str(data['user_id'])
    else:
        # no user id posted
        status_code = 400
        return status_code
    try:
        file_path = get_working_dir() + '/app/webapp/tweets_following/' + user_id + '.json'
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                tweet_data = json.load(json_file)
        else:
            tweet_data = {'following': []}
        status_code = 200
        return jsonify(tweet_data), status_code
    except:
        status_code = 444
        return status_code


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

                topics = predict_topic_en(tweet_text)
                topic_list = []
                for key, value in topics.items():
                    if value > 0.5:
                        topic_list.append(key)
                analysis_results['topics'] = topic_list

                with open(get_working_dir() + '/app/webapp/analysis_results/' + file, 'w') as json_file:
                    json.dump(analysis_results, json_file)

        for folder in os.listdir(get_working_dir() + '/app/webapp/tweets_users'):
            user_sentiment = {'negative': [], 'neutral': [], 'positive': []}
            user_emotion = {'sadness': [], 'anger': [], 'joy': [], 'optimism': []}
            user_topics = []
            for file in os.listdir(get_working_dir() + '/app/webapp/tweets_users/' + folder):
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

                    topics = predict_topic_en(tweet_text)
                    topic_list = []
                    for key, value in topics.items():
                        if value > 0.5:
                            topic_list.append(key)
                    user_tweet_sentiment = ['neg', 'neu', 'pos'][[neg, neu, pos].index(max([neg, neu, pos]))]
                    user_topics.append({'topics': topic_list, 'sentiment': user_tweet_sentiment})

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
            analysis_results['topics'] = user_topics

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
        clear_demo_data()

        stream = initialize_stream()
        stream_stats = {'users': 0,
                        'topics': 0,
                        'following': 0}

        home_tweets = get_home_timeline_tweets(stream)
        users = []
        topics = []
        for tweet in home_tweets:
            topics += get_tweet_topic(tweet)
            users.append(tweet['user']['id_str'])
            save_home_tweet(tweet)

        topics = list(set(topics))
        for topic in topics:
            if stream_stats['topics'] >= 180:
                print('sleeping for 15min to get new topics...')
                time.sleep(901)
                stream_stats['topics'] = 0
            print(topic)
            create_new_topic_folder(topic)
            topic_tweets = search_tweets(stream, topic)
            for topic_tweet in topic_tweets:
                save_topic_tweet(topic_tweet, topic)
            stream_stats['topics'] += 1

        all_following_ids = []
        for user_id in users:
            if stream_stats['users'] >= 900:
                print('sleeping for 15min to get new users...')
                time.sleep(901)
                stream_stats['users'] = 0
            if stream_stats['following'] >= 15:
                print('sleeping for 15min to get new following...')
                time.sleep(901)
                stream_stats['following'] = 0
            create_new_user_folder(user_id)
            user_tweets = get_user_timeline_tweets(stream, user_id)
            for user_tweet in user_tweets:
                save_user_tweet(user_tweet, user_id)
            user_following_ids = get_users_following_ids(stream, user_id)
            save_followed_users(user_following_ids, user_id)
            all_following_ids += user_following_ids
            stream_stats['users'] += 1
            stream_stats['following'] += 1

        for user_id in all_following_ids:
            if stream_stats['users'] >= 900:
                print('sleeping for 15min to get new users...')
                time.sleep(901)
                stream_stats['users'] = 0
            dir_path = get_working_dir() + '/app/webapp/tweets_users/' + user_id
            if not os.path.exists(dir_path):
                create_new_user_folder(user_id)
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
        user_id = str(data['user_id'])
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        file_path = get_working_dir() + '/app/webapp/analysis_results/tweets_users/' + user_id + '.json'
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                analysis_results = json.load(json_file)
        else:
            analysis_results = {'sentiment': {}, 'emotion': {}, 'topics': []}
        status_code = 200
    except:
        # error
        analysis_results = {}
        status_code = 444
    return jsonify(analysis_results), status_code


@api_blueprint.route("identify_echo_chambers/", methods=["POST"])
def identify_echo_chambers():
    """
    Identify echo chambers in topic/sentiment lists.
    """
    data = request.json
    if 'topics' in data and 'sentiments' in data:
        topics = data['topics']
        sentiments = data['sentiments']
    else:
        # no information posted
        status_code = 400
        return status_code
    try:
        num_labels = len(list(set(sentiments)))
        analysis_results = {}
        for idx, value in enumerate(topics):
            value = value.replace('_', ' ')
            if value not in analysis_results:
                analysis_results[value] = [0] * num_labels
            if sentiments[idx] == 'neg':
                analysis_results[value][0] += 1
            elif sentiments[idx] == 'neu':
                analysis_results[value][1] += 1
            elif sentiments[idx] == 'pos' and num_labels == 3:
                analysis_results[value][2] += 1
            elif sentiments[idx] == 'pos' and num_labels == 2:
                analysis_results[value][1] += 1
        for key, value in analysis_results.items():
            if sum(value) > 3:
                new_sentiment_scores = []
                for sentiment_score in value:
                    new_sentiment_scores.append(sentiment_score/sum(value))
                analysis_results[key] = new_sentiment_scores
            else:
                analysis_results[key] = [0]
        echo_chambers = {}
        for topic, sentiments in analysis_results.items():
            if max(sentiments) >= 0.85 and len(sentiments) == 3:
                echo_chambers[topic] = ['neg', 'neu', 'pos'][sentiments.index(max(sentiments))]
            elif max(sentiments) >= 0.85 and len(sentiments) == 2:
                echo_chambers[topic] = ['neg', 'pos'][sentiments.index(max(sentiments))]
        status_code = 200
    except:
        # error
        echo_chambers = {}
        status_code = 444
    return jsonify(echo_chambers), status_code


@api_blueprint.route("load_topic_data_EXP/", methods=["POST"])
def load_topic_data_EXP():
    """
    Load tweets on specific topic for language specific demo page.
    """
    data = request.json
    if 'topic' in data:
        topic = data['topic'].lower()
        n = int(data['n'])
    else:
        # no topic posted
        status_code = 400
        return status_code
    lang = 'it'
    if 'lang' in data and data['lang'] in ['it', 'en']:
        lang = data['lang']
    if lang == 'it':
        lang = 'italian'
    elif lang == 'en':
        lang = 'english'
    topics_available = [topic_name.split('.')[0] for topic_name in os.listdir(get_working_dir() + '/app/webapp/' + lang + '_demo/data/topics/')
                        if topic_name.endswith('json')]
    if topic not in topics_available:
        status_code = 200
        tweet_results = {'tweets': [], 'analysis': []}
        return jsonify(tweet_results), status_code
    try:
        with open(get_working_dir() + '/app/webapp/' + lang + '_demo/data/topics/' + topic + '.json') as json_file:
            tweet_data = json.load(json_file)
        if n > 0:
            idc = random.sample(range(len(tweet_data['tweets'])), n)
            tweet_results = {'tweets': [], 'analysis': []}
            for idx in idc:
                tweet_results['tweets'].append(tweet_data['tweets'][idx])
                tweet_results['analysis'].append(tweet_data['analysis'][idx])
            status_code = 200
            return jsonify(tweet_results), status_code
        else:
            if lang == 'english' or lang == 'italian':
                data = list(zip(tweet_data['tweets'], tweet_data['analysis']))
                random.Random(4).shuffle(data)
                tweets, analysis = zip(*data)
                tweet_data = {}
                tweet_data['tweets'] = tweets
                tweet_data['analysis'] = analysis
            status_code = 200
            return jsonify(tweet_data), status_code
    except:
        status_code = 444
        return status_code


@api_blueprint.route("load_user_data_EXP/", methods=["POST"])
def load_user_data_EXP():
    """
    Load tweets of specific user for language specific demo page.
    """
    data = request.json
    if 'user_id' in data:
        user_id = str(data['user_id'])
    else:
        # no user id posted
        status_code = 400
        return status_code
    lang = 'it'
    if 'lang' in data and data['lang'] in ['it', 'en']:
        lang = data['lang']
    if lang == 'it':
        lang = 'italian'
    elif lang == 'en':
        lang = 'english'
    try:
        file_path = get_working_dir() + '/app/webapp/' + lang + '_demo/data/users/' + user_id + '.json'
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                tweet_data = json.load(json_file)
        else:
            tweet_data = {'tweets': [], 'analysis': [{'sentiment': {}, 'emotion': {}, 'topics': []}]}
        if len(tweet_data['analysis']) == 0:
            tweet_data = {'tweets': [], 'analysis': [{'sentiment': {}, 'emotion': {}, 'topics': []}]}
        status_code = 200
        return jsonify(tweet_data), status_code
    except:
        status_code = 444
        return status_code


@api_blueprint.route("load_user_following_data_EXP/", methods=["POST"])
def load_user_following_data_EXP():
    """
    Load list of following ids of specific user for language specific demo page.
    """
    data = request.json
    if 'user_id' in data:
        user_id = str(data['user_id'])
    else:
        # no user id posted
        status_code = 400
        return status_code
    lang = 'it'
    if 'lang' in data and data['lang'] in ['it', 'en']:
        lang = data['lang']
    if lang == 'it':
        lang = 'italian'
    elif lang == 'en':
        lang = 'english'
    try:
        file_path = get_working_dir() + '/app/webapp/' + lang + '_demo/data/following/' + user_id + '.json'
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                tweet_data = json.load(json_file)
        else:
            tweet_data = {'following': []}
        status_code = 200
        return jsonify(tweet_data), status_code
    except:
        status_code = 444
        return status_code


@api_blueprint.route("crawl_new_data_IT/", methods=["POST"])
def crawl_new_data_IT():
    """
    Crawl new data for Italian Twitter demo.
    """
    data = request.json
    if 'topics' in data:
        topics = data['topics']
        crawl_new_topics = True
    else:
        # no topics posted
        crawl_new_topics = False
    if 'clear' in data:
        clear_data = data['clear']
    else:
        clear_data = False
    try:
        if clear_data:
            clear_italian_demo_data()

        stream = initialize_stream()
        stream_stats = {'users': 0,
                        'topics': 0,
                        'following': 0}

        users = []
        if crawl_new_topics:
            for topic in topics:
                print(topic)
                if stream_stats['topics'] >= 180:
                    print('sleeping for 15min to get new topics...')
                    time.sleep(901)
                    stream_stats['users'] = 0
                    stream_stats['topics'] = 0
                    stream_stats['following'] = 0
                topic_tweets = search_tweets(stream, topic, language='it')
                for t in topic_tweets:
                    users.append(t['user']['id_str'])
                save_topic_tweets_italian(topic_tweets, topic)
                stream_stats['topics'] += 1
        else:
            for topic_file in os.listdir(get_working_dir() + '/app/webapp/italian_demo/data/topics/'):
                with open(get_working_dir() + '/app/webapp/italian_demo/data/topics/' + topic_file) as json_file:
                    tweet_data = json.load(json_file)
                for t in tweet_data['tweets']:
                    users.append(t['user']['id_str'])

        all_following_ids = []
        for user_id in users:
            if stream_stats['users'] >= 900:
                print('sleeping for 15min to get new users...')
                time.sleep(901)
                stream_stats['users'] = 0
                stream_stats['topics'] = 0
                stream_stats['following'] = 0
            if stream_stats['following'] >= 15:
                print('sleeping for 15min to get new following information...')
                time.sleep(901)
                stream_stats['users'] = 0
                stream_stats['topics'] = 0
                stream_stats['following'] = 0
            print(user_id)
            try:
                user_tweets = get_user_timeline_tweets(stream, user_id)
                save_user_tweets_italian(user_tweets, user_id)
                user_following_ids = get_users_following_ids(stream, user_id)
                save_followed_users_italian(user_following_ids, user_id)
                all_following_ids += user_following_ids
            except:
                pass
            stream_stats['users'] += 1
            stream_stats['following'] += 1

        for user_id in all_following_ids:
            if stream_stats['users'] >= 900:
                print('sleeping for 15min to get new users...')
                time.sleep(901)
                stream_stats['users'] = 0
                stream_stats['topics'] = 0
                stream_stats['following'] = 0
            print(user_id)
            try:
                user_tweets = get_user_timeline_tweets(stream, user_id)
                save_user_tweets_italian(user_tweets, user_id)
            except:
                pass
            stream_stats['users'] += 1

        status_code = 200
        res = {"status": 'SUCCESSFUL'}
    except:
        status_code = 444
        res = {"status": 'ERROR'}
    return jsonify(res), status_code


@api_blueprint.route("analyze_twitter_data_IT/", methods=["GET"])
def analyze_twitter_data_IT():
    """
    Run analysis algorithms on available Italian demo tweets.
    """
    try:
        for file in os.listdir(get_working_dir() + '/app/webapp/italian_demo/data/topics'):
            if file.endswith('json'):
                print('processing topic...', file)
                with open(get_working_dir() + '/app/webapp/italian_demo/data/topics/' + file, 'r') as json_file_input:
                    topic_content = json.load(json_file_input)
                topic_content['analysis'] = []
                for tweet in topic_content['tweets']:
                    analysis_results = {}
                    tweet_text = tweet['text']
                    neg, pos = predict_sentiment_it(tweet_text)
                    analysis_results['sentiment'] = {'negative': neg, 'positive': pos}
                    analysis_results['emotion'] = predict_emotion_it(tweet_text)
                    tweet_text_en = translate_it_en(tweet_text)
                    topics = predict_topic_en(tweet_text_en['translation_text'])
                    topic_list = []
                    for key, value in topics.items():
                        if value > 0.5:
                            topic_list.append(key)
                    analysis_results['topics'] = topic_list
                    analysis_results['hate_speech'] = predict_hate_speech_en_facebook(tweet_text_en['translation_text'])
                    topic_content['analysis'].append(analysis_results)
                with open(get_working_dir() + '/app/webapp/italian_demo/data/topics/' + file, 'w') as json_file_output:
                    json.dump(topic_content, json_file_output)

        for file in os.listdir(get_working_dir() + '/app/webapp/italian_demo/data/users'):
            if file.endswith('json'):
                print('processing user...', file)
                user_sentiment = {'negative': [], 'positive': []}
                user_emotion = {'anger': [], 'fear': [], 'joy': [], 'sadness': []}
                user_topics = []
                with open(get_working_dir() + '/app/webapp/italian_demo/data/users/' + file, 'r') as json_file_input:
                    user_content = json.load(json_file_input)
                user_content['analysis'] = []
                if len(user_content['tweets']) > 0:
                    for tweet in user_content['tweets']:
                        tweet_text = tweet['text']
                        neg, pos = predict_sentiment_it(tweet_text)
                        user_sentiment['negative'].append(neg)
                        user_sentiment['positive'].append(pos)
                        emotion_results = predict_emotion_it(tweet_text)
                        user_emotion['anger'].append(emotion_results['anger'])
                        user_emotion['fear'].append(emotion_results['fear'])
                        user_emotion['joy'].append(emotion_results['joy'])
                        user_emotion['sadness'].append(emotion_results['sadness'])
                        tweet_text_en = translate_it_en(tweet_text)
                        topics = predict_topic_en(tweet_text_en['translation_text'])
                        topic_list = []
                        for key, value in topics.items():
                            if value > 0.5:
                                topic_list.append(key)
                        user_tweet_sentiment = ['neg', 'pos'][[neg, pos].index(max([neg, pos]))]
                        user_topics.append({'topics': topic_list, 'sentiment': user_tweet_sentiment})
                    user_sentiment = {key: sum(value) / len(value) for key, value in user_sentiment.items()}
                    user_emotion = {key: sum(value) / len(value) for key, value in user_emotion.items()}
                    analysis_results = {'sentiment': {}, 'emotion': {}}
                    sum_all_sentiment = sum([user_sentiment['negative'], user_sentiment['positive']])
                    analysis_results['sentiment']['negative'] = user_sentiment['negative'] / sum_all_sentiment
                    analysis_results['sentiment']['positive'] = user_sentiment['positive'] / sum_all_sentiment
                    sum_all_emotion = sum(
                        [user_emotion['anger'], user_emotion['fear'], user_emotion['joy'], user_emotion['sadness']])
                    analysis_results['emotion']['anger'] = user_emotion['anger'] / sum_all_emotion
                    analysis_results['emotion']['fear'] = user_emotion['fear'] / sum_all_emotion
                    analysis_results['emotion']['joy'] = user_emotion['joy'] / sum_all_emotion
                    analysis_results['emotion']['sadness'] = user_emotion['sadness'] / sum_all_emotion
                    analysis_results['topics'] = user_topics
                    user_content['analysis'].append(analysis_results)
                with open(get_working_dir() + '/app/webapp/italian_demo/data/users/' + file, 'w') as json_file_output:
                    json.dump(user_content, json_file_output)
        status_code = 200
        res = {"status": 'SUCCESSFUL'}
    except:
        status_code = 444
        res = {"status": 'ERROR'}
    return jsonify(res), status_code


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


@api_blueprint.route("EN/hate_speech_facebook/", methods=["POST"])
def predict_hate_speech_english_facebook():
    """
    Predict whether an English text contains hate speech or not (trained by facebook on a diverse dataset).
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        not_hate, hate = predict_hate_speech_en_facebook(text)
        output = json.dumps({'not hate': not_hate,
                             'hate': hate})
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


@api_blueprint.route("EN/topics/", methods=["POST"])
def identify_topics_english():
    """
    Identify topics of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        topics = predict_topic_en(text)
        topic_list = []
        for key, value in topics.items():
            if value > 0.5:
                topic_list.append(key)
        output = json.dumps({'topics': topic_list})
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code


@api_blueprint.route("EN/topics_cip/", methods=["POST"])
def identify_cip_topics_english():
    """
    Identify topics of an English Text.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        topics = predict_cip_topic(text)
        topic = ''
        for key, value in topics.items():
            if value >= 0.5:
                topic = key
        output = json.dumps({'topic': topic})
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


##########################
# # # CROSS LINGUAL # # #
##########################

@api_blueprint.route("cross_lingual/IT_EN/", methods=["POST"])
def translate_italian_to_english():
    """
    Translate an Italian text to English.
    """
    data = request.json
    if 'text' in data:
        text = data['text']
    else:
        # no text posted
        status_code = 400
        return status_code
    try:
        translation = translate_it_en(text)
        output = json.dumps(translation)
        status_code = 200
    except:
        # error
        output = ""
        status_code = 444
    return output, status_code
