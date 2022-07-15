import os
import json
from twython import Twython
from courage_algorithms.scripts.path_setup import get_working_dir


def load_twitter_keys():
    file_path = get_working_dir() + '/app/webapp/twitter_keys.json'
    with open(file_path) as fp:
        twitter_keys = json.load(fp)
    return twitter_keys


def initialize_stream():
    AUTH_KEYS = load_twitter_keys()
    stream = Twython(app_key=AUTH_KEYS["app_key"],
                     app_secret=AUTH_KEYS["app_secret"],
                     oauth_token=AUTH_KEYS["oauth_token"],
                     oauth_token_secret=AUTH_KEYS["oauth_token_secret"],
                     client_args={'timeout': 30})
    return stream


def get_home_timeline_tweets(stream): # 20
    home_timeline_tweets = stream.get_home_timeline(tweet_mode='extended')
    if len(home_timeline_tweets) > 0:
        for idx, tweet in enumerate(home_timeline_tweets):
            tweet['text'] = tweet['full_text']
            home_timeline_tweets[idx] = tweet
    return home_timeline_tweets


def get_user_timeline_tweets(stream, user_id): # 20
    timeline_tweets = stream.get_user_timeline(user_id=user_id, tweet_mode='extended')
    if len(timeline_tweets) > 0:
        for idx, tweet in enumerate(timeline_tweets):
            tweet['text'] = tweet['full_text']
            timeline_tweets[idx] = tweet
    return timeline_tweets


def search_tweets(stream, search_query): # 15
    matching_tweets = stream.search(q=search_query, lang='en', tweet_mode='extended')
    matching_tweets = matching_tweets['statuses']
    if len(matching_tweets) > 0:
        for idx, tweet in enumerate(matching_tweets):
            tweet['text'] = tweet['full_text']
            matching_tweets[idx] = tweet
    return matching_tweets


def save_home_tweet(tweet):
    file_path = get_working_dir() + '/app/webapp/tweets/' + tweet['id_str'] + '.json'
    with open(file_path, 'w') as fp:
        json.dump(tweet, fp)


def save_topic_tweet(tweet, topic):
    file_path = get_working_dir() + '/app/webapp/tweets_topics/' + topic + '/' + tweet['id_str'] + '.json'
    with open(file_path, 'w') as fp:
        json.dump(tweet, fp)


def save_user_tweet(tweet, user_id):
    file_path = get_working_dir() + '/app/webapp/tweets_users/' + user_id + '/' + tweet['id_str'] + '.json'
    with open(file_path, 'w') as fp:
        json.dump(tweet, fp)


def create_new_topic_folder(topic):
    dir_path = get_working_dir() + '/app/webapp/tweets_topics/' + topic
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def create_new_user_folder(user_id):
    dir_path = get_working_dir() + '/app/webapp/tweets_users/' + user_id
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_tweet_topic(tweet):
    hashtags = tweet['entities']['hashtags']
    hashtags_clean = []
    for h in hashtags:
        hashtags_clean.append(h['text'].lower())
    return hashtags_clean
