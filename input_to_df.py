import os
import csv
import json
import pickle
import pandas as pd
import math

test_dir =    '/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/charliehebdo-all-rnr-threads/rumours/552783238415265792'

def get_file_path(dirName):
    '''

    :param dirName: direction of the directory of all data
    :return: a list of file directions in that directory
    '''
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    print('listoffiles',listOfFiles)
    return listOfFiles


def get_tweets_addresses(list_of_files):
    # TODO add code to get replies and structure of replies
    '''

    :param list_of_files: a list of all files in directory
    :return: a list of all source tweets
    '''
    tweets = []
    for elem in list_of_files:
        elem = str(elem)
        parts = elem.split('/')
        if parts[-2] == "source-tweets":
            tweets.append(elem)
    print('tweets',tweets)
    return tweets


def make_source_df(list_of_tweets):
    '''
    get from the list of tweets addresses tweets and extract all features to for feature selection
    :param list_of_tweets: a list of addresses of tweets
    :return: a json/pickle/pandas df of :
    ID  TEXT    features    CLASS(rumour not rumour)
    features:

    '''
    # classification 1 -> rumours
    # classification 0 -> non-rumours
    #TODO add text based features here too to select the right features
    id_feature_class = {}
    for address in list_of_tweets:
        parts = address.split('/')
        tweet_id = parts[-3]
        with open(address) as f:
            tweet = json.load(f)
            classification = 0
            if parts[-4] == "rumours":
                classification = 1
            id_feature_class[tweet_id] = {"classification": classification, "text": tweet['text'],
                                          "favorite_count_log": math.log(tweet['favorite_count']+1),
                                          "retweet_count": math.log(tweet['retweet_count']+1),
                                          "verified": tweet['user']['verified'],
                                          "followers": tweet['user']['followers_count'],
                                          "follow_ratio": (tweet['user']['followers_count']+1)/(tweet['user']['friends_count']+1)
                                          }
            print('id_feature_class',id_feature_class)
                # if "media" in data:
                #     id_feature_class[single_id]["media_type"] = data["media"][0]["media_type"]

    with open('source_id_feature_class_n.json', 'w') as fp:
        json.dump(id_feature_class, fp)
    return id_feature_class


def make_visualization_reply_df(devdir, list_of_tweets):
    '''
    iput:
        dev dir: direction of dev wich has id-tag of source in subtask b
        list_of_tweets: a list of id-address
    output:
        a json/df of id features and classification
            id
            text
            media type
            favorite_count
            retweet_count
            verified
            followers

    '''
    id_feature_class = {}
    with open(devdir) as f:
        ids = json.load(f)
        tweets_dic = list_of_tweets
        ids = ids["subtaskaenglish"]
        for single_id in ids:
            with open(tweets_dic[single_id]) as g:
                data = json.load(g)
                id_feature_class[single_id] = {"classification": ids[single_id], "text": data['text'],
                                               "favorite_count": data['favorite_count'],
                                               "retweet_count": data['retweet_count'],
                                               "verified": data['user']['verified'],
                                               "followers": data['user']['followers_count']}
                # if  "media" in data:
                #     id_feature_class[single_id]["media_type"]=data["media"][0]["media_type"]
                #     print("he")
    with open('replies_id_feature_class.json', 'w') as fp:
        json.dump(id_feature_class, fp)
    return id_feature_class


def test(dirname):
    list_of_files = get_file_path(dirname)
    list_of_tweets=get_tweets_addresses(list_of_files)
    return make_source_df(list_of_tweets)


# structures, tweets=test("/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/twitter-english")
# source_id_feature_class=make_visualization_source_df('/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/tweets-train-key.json',tweets)
# make_visualization_reply_df('/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/tweets-train-key.json',tweets)
def make_panda_df(dir):
    '''

    :param dir: input address of json of id_feature_class.json
    :return: a pickle of pandafied dataframe of to visualize data
    '''
    with open(dir) as inputjson:
        data = json.load(inputjson)
        data_pd = pd.DataFrame.from_dict(data)
        output_address ="df_id_feature_class.json"
        output = data_pd.T.to_json(output_address)
test(test_dir)



