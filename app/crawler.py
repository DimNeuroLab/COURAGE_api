import os
import json
from twython import Twython
from datetime import datetime
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


def load_existing_home_timeline_tweets_with_date():
    tweets = []
    for file in os.listdir(get_working_dir() + '/app/webapp/tweets'):
        if file.endswith('json'):
            with open(get_working_dir() + '/app/webapp/tweets/' + file) as json_file:
                tweet_data = json.load(json_file)
            tweets.append((tweet_data['id_str'], datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
    return tweets


def get_home_timeline_tweets(stream): # 20
    home_timeline_tweets = stream.get_home_timeline(tweet_mode='extended')
    if len(home_timeline_tweets) > 0:
        for idx, tweet in enumerate(home_timeline_tweets):
            tweet['text'] = tweet['full_text']
            home_timeline_tweets[idx] = tweet
    return home_timeline_tweets


def get_user_timeline_tweets(stream, user_id, n=10): # 20
    timeline_tweets = stream.get_user_timeline(user_id=user_id, tweet_mode='extended', count=n, exclude_replies=True)
    if len(timeline_tweets) > 0:
        for idx, tweet in enumerate(timeline_tweets):
            tweet['text'] = tweet['full_text']
            timeline_tweets[idx] = tweet
    return timeline_tweets


def search_tweets(stream, search_query, language='en', num_tweets=15): # 15
    search_query += ' -RT'
    matching_tweets = stream.search(q=search_query, lang=language, tweet_mode='extended', count=num_tweets)
    matching_tweets = matching_tweets['statuses']
    if len(matching_tweets) > 0:
        for idx, tweet in enumerate(matching_tweets):
            tweet['text'] = tweet['full_text']
            matching_tweets[idx] = tweet
    return matching_tweets


def get_users_following_ids(stream, user_id, num_followers=15):
    following_ids = stream.get_friends_ids(user_id=user_id, count=num_followers)
    return following_ids['ids']


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


def save_followed_users(following_id_list, user_id):
    file_path = get_working_dir() + '/app/webapp/tweets_following/' + str(user_id) + '.json'
    file_content = {'following': following_id_list}
    with open(file_path, 'w') as fp:
        json.dump(file_content, fp)


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


def delete_home_timeline_dir():
    dir_path = get_working_dir() + '/app/webapp/tweets'
    for file in os.listdir(dir_path):
        file_path = dir_path + '/' + file
        os.remove(file_path)
    dir_path = get_working_dir() + '/app/webapp/analysis_results'
    for file in os.listdir(dir_path):
        if file.endswith('json'):
            file_path = dir_path + '/' + file
            os.remove(file_path)


def delete_topic_tweet_dir(topic):
    dir_path = get_working_dir() + '/app/webapp/tweets_topics/' + topic
    for file in os.listdir(dir_path):
        file_path = dir_path + '/' + file
        os.remove(file_path)
    os.rmdir(dir_path)


def delete_user_tweet_dir(user_id):
    dir_path = get_working_dir() + '/app/webapp/tweets_users/' + user_id
    for file in os.listdir(dir_path):
        file_path = dir_path + '/' + file
        os.remove(file_path)
    os.rmdir(dir_path)
    file_path = get_working_dir() + '/app/webapp/analysis_results/tweets_users/' + user_id + '.json'
    os.remove(file_path)


def delete_user_followed_dir(user_id):
    file_path = get_working_dir() + '/app/webapp/tweets_following/' + user_id + '.json'
    os.remove(file_path)


def clear_demo_data():
    delete_home_timeline_dir()
    for tweet_topic in os.listdir(get_working_dir() + '/app/webapp/tweets_topics'):
        delete_topic_tweet_dir(tweet_topic)
    for tweet_user in os.listdir(get_working_dir() + '/app/webapp/tweets_users'):
        delete_user_tweet_dir(tweet_user)
    for user_id in os.listdir(get_working_dir() + '/app/webapp/tweets_following'):
        delete_user_followed_dir(user_id)


def save_topic_tweets_italian(tweet_list, topic):
    file_path = get_working_dir() + '/app/webapp/italian_demo/data/topics/' + topic + '.json'
    file_content = {'tweets': tweet_list, 'analysis': []}
    with open(file_path, 'w') as fp:
        json.dump(file_content, fp)


def save_user_tweets_italian(tweet_list, user_id):
    file_path = get_working_dir() + '/app/webapp/italian_demo/data/users/' + user_id + '.json'
    file_content = {'tweets': tweet_list, 'analysis': []}
    with open(file_path, 'w') as fp:
        json.dump(file_content, fp)


def save_followed_users_italian(following_id_list, user_id):
    file_path = get_working_dir() + '/app/webapp/italian_demo/data/following/' + str(user_id) + '.json'
    file_content = {'following': following_id_list}
    with open(file_path, 'w') as fp:
        json.dump(file_content, fp)


def clear_italian_demo_data():
    data_path = get_working_dir() + '/app/webapp/italian_demo/data/'
    for folder in ['following', 'topic', 'users']:
        folder_path = data_path + folder
        for file in os.listdir(folder_path):
            file_path = folder_path + '/' + file
            os.remove(file_path)
