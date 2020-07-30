import os
import csv
import json
import pickle
import pandas as pd
def get_file_path(dirName):
    # # Get the list of all files in directory tree at given path

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    return listOfFiles


def make_df(list_of_files):
    # # Make a list of structures addreses
    # make a list of id and json of  tweets
    '''
    returns:
        tweets: id-address
        structure: list of structures
    '''
    structures = []
    tweets = {}
    for elem in list_of_files:
        elem = str(elem)
        if elem.endswith("structure.json"):
            structures += [elem]
        elif elem.endswith("json"):
            tweets[elem[:-5].rsplit('/',1)[-1]]=elem
    return structures, tweets
def make_visualization_source_df(devdir,list_of_tweets):
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
    id_feature_class={}
    with open(devdir) as f:
        ids = json.load(f)
        tweets_dic=list_of_tweets
        ids=ids["subtaskbenglish"]
        for single_id in ids:
            with open(tweets_dic[single_id]) as g:
                data=json.load(g)
                id_feature_class[single_id]={"classification":ids[single_id],"text":data['text'],"favorite_count":data['favorite_count'],"retweet_count":data['retweet_count'],"verified":data['user']['verified'],"followers":data['user']['followers_count']}
    with open('test_id_feature_class.json', 'w') as fp:
        json.dump(id_feature_class, fp)
    return id_feature_class
def test(dirname):
    list_of_files=get_file_path(dirname)
    return make_df(list_of_files)
# structures, tweets=test("/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/twitter-english")
# id_feature_class=make_visualization_source_df('/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/tweets-train-key.json',tweets)
def make_panda_df(dir):
    '''

    :param dir: input address of json of id_feature_class.json
    :return: a pickle of pandafied dataframe of to visualize data
    '''
