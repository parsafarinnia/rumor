import os
l=[1,2,3]
import csv
import json
import pickle
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
if __name__ == '__main__':
    test_string="atic video via @josh_wingrove of shots fired inside parliament building: https://t.co/1waid25vOE #Ottawa #shooting 123 UPER ,, the the the"
    test_string=' '.join(word for word in test_string.split(' ') if not word.startswith('@'))
    tokens=word_tokenize(test_string)
    # lower
    tokens = [w.lower() for w in tokens]
    #remove usernames
    tokens  = [word for word in tokens if "@" not in word]
    # # punctuation
    # table = str.maketrans('', '', string.punctuation)
    # stripped = [w.translate(table) for w in tokens]
    # words = [word for word in stripped if word.isalpha()]
    # #stop words
    # stop_words = set(stopwords.words('english'))
    # stop_words.add('https')
    # words = [w for w in words if not w in stop_words]
    # # stemmer
    # porter = PorterStemmer()
    # words = [porter.stem(word) for word in words]


    print(tokens)
