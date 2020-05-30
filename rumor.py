import os
import csv
import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
'''
    For the given path, get the List of all files in the directory tree 
'''
direct = '/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/twitter-english'


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

    structures = []
    tweets = []
    for elem in list_of_files:
        elem = str(elem)
        if elem.endswith("structure.json"):
            structures += [elem]
        elif elem.endswith("json"):
            tweets += [elem]
    return structures, tweets


def make_cvs(direct):
    list_of_files = get_file_path(direct)
    structures, tweets = make_df(list_of_files)
    tweets_dic={}
    # print(list_of_files)
    with open('structure.csv', 'w', newline='') as t:
        for item in structures:
            f = open(item, "r")
            s = str(f.readline())
            t.write(s)
            f.close()
    t.close()
    with open('tweets.csv', 'w', newline='') as a:
        for item in tweets:
            # keep file az string
            # f = open(item, "r")
            # s = str(f.readline())
            # s = item[-23:-5] + ',' + s
            # a.write(s)
            # f.close()
            # just keep the main text
            with open(item) as f:
                data=json.load(f)
            tweets_dic[item[-23:-5]]=str(data["text"])
            s=item[-23:-5] + ','+str(data["text"])+'\n'
            a.write(s)
            f.close()

    a.close()
    '''write a dictionary and save it to pickle with id and text'''
    with open('tweets.pickle','wb') as handler:
        pickle.dump(tweets_dic,handler,protocol=pickle.HIGHEST_PROTOCOL)
    handler.close()
# def get_source(dr):
#     with open('source_tweets.csv','w',newline=' ')as a;
#         line=open(dr,"r")
#         s=str(line.readline())
'''combine id text and class for tweets
and give a array like :
ID|text|class

'''
def combine_text_id_classification(tweets,classifications,dev):
    '''

    :param tweets: id-text
    :param classifications: id-classification
    :return:
    '''
    id_text_class={}
    with open(classifications) as f:
        data = json.load(f)
        with open(tweets,'rb') as t:
            tweets_dic=pickle.load(t)
            data=data["subtaskaenglish"]
            for item in data:
                id_text_class[item]={"text":tweets_dic[item],"class":data[item]}
    type=dev+'id_text_class.json'
    with open(type, 'w') as fp:
        json.dump(id_text_class, fp)

def clean_text(test_string):
    '''

    :param test_string: get a string text
    :return: a list of tokens
    '''
    #remove usernames
    test_string = ' '.join(word for word in test_string.split(' ') if not word.startswith('@'))
    tokens=word_tokenize(test_string)
    # lower
    tokens = [w.lower() for w in tokens]

    # punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    #stop words
    stop_words = set(stopwords.words('english'))
    stop_words.add('https')
    words = [w for w in words if not w in stop_words]
    # stemmer
    porter = PorterStemmer()
    words = [porter.stem(word) for word in words]
    return words
def vectorize(path):
    '''
    vocabulary is 6000 words
    get all data vectorize data and return vector space
    :return:
    '''
    map_class={"comment":0,"deny":1,"support":2,"query":3}
    classification=[]
    with open(path) as f:
        tweets_json=json.load(f)
        corpus=[]
        for item in tweets_json:
            print(item)
            words=clean_text(tweets_json[item]["text"])
            classification.append(map_class[tweets_json[item]["class"]])
            s=""
            for token in words:
                s=s+" "+token
            corpus.append(s)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(X.shape)
    return corpus,X,classification
if __name__ == '__main__':
    structures_list = []
    # classes='/Users/macbook/Desktop/reasearch/rumoureval2019/rumoureval-2019-training-data/tweets-train-key.json'
    # tweets='/Users/macbook/Desktop/reasearch/rumor/rumor/tweets.pickle'
    # combine_text_id_classification(tweets,classes,"train")
    # make_cvs(direct)

    vs,x,y=vectorize('/Users/macbook/Desktop/reasearch/rumor/rumor/train_id_text_class.json')