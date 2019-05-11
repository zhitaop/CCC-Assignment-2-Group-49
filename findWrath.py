import json
import numpy as np
import pandas as pd
import math
from pandas import DataFrame, Series
from glom import glom
from interval import Interval
from collections import Counter
import re
from textblob import TextBlob
import nltk
from shapely.geometry import shape, Point
from nltk.corpus import wordnet

# with open("/Users/Vanmir/Documents/2019Winter/comp90024/melbGrid.json", 'r') as load_f:
#     melb_grid = json.load(load_f)
# 
# with open("/Users/Vanmir/Documents/2019Winter/comp90024/smallTwitter.json", 'r') as load_f:
#     small_twit = json.load(load_f)

# read file
with open("/Users/Vanmir/Desktop/vic_lga.json", 'r') as file:
    line = file.readline()
    vic_lga = json.loads(line)

#twitter info
twitterfile1 = "/Users/Vanmir/Desktop/largetest.json"


def read_twi_coors(record):
    coordinate = record['coordinates']
    if coordinate:
        return coordinate['coordinates']
    else:
        coordinate = record['place']['bounding_box']['coordinates'][0][0]
        return coordinate


def find_lga_area(lga_info, record):
    coordinate = read_twi_coors(record)
    lga_geo = lga_info['features']
    for coor in lga_geo:
        if Point(coordinate).within(shape(coor['geometry'])):
            return coor['properties']['vic_lga__3']
    return False


def find_contain_set(wrath_set, twi_set):
    contain_set = [word for word in wrath_set if word in twi_set]
    if contain_set:
        return True
    else:
        return False


twitts = DataFrame(columns=['text', 'lga_area'])
dict2 = {}
dict2['rows'] = []

with open(twitterfile1, encoding='utf-8') as twitter:
    line = twitter.readline()
    # line = twitter.readline()
    while (line != ''):
        line = line.strip(',\n')
        record = json.loads(line)
        dict1 = {}
        dict3 = {}
        lga_area = find_lga_area(vic_lga, record)
        if lga_area is not False:
            dict1['lga_area'] = lga_area
            text = record['text']
            # remove hyperlink
            text = re.sub(r'http\S+', '', text)
            # remove html entities
            text = re.sub(r'\&\w*;', '', text)
            # remove @user
            text = re.sub('@[^\s]+', '', text)
            text = nltk.word_tokenize(text.lower())
            dict1['text'] = text
            twitts = twitts.append(dict1, ignore_index=True)
            dict3['coordinates'] = read_twi_coors(record)
            dict2['rows'].append(dict3)
            line = twitter.readline()
        else:
            line = twitter.readline()

total_counts = {}
a = twitts['lga_area'].value_counts()
total_counts['rows'] = []
for i in range(len(a)):
    dict11 = {}
    dict11['name'] = a.keys()[i]
    dict11['count'] = a[i].item()
    total_counts['rows'].append(dict11)

score = []
for i in range(len(twitts)):
    blob = TextBlob(twitts.loc[i, 'text'])
    score.append(blob.sentiment.polarity)
twitts['score'] = score

temp = twitts[twitts["score"] < 0]


# find key words
def find_contain_set(wrath_set, twi_set):
    contain_set = [word for word in wrath_set if word in twi_set]
    if contain_set:
        return True
    else:
        return False


syns_list = []
list = ['hate', 'angry', 'offended', 'snap', 'pissed', 'mad', 'foolish', 'stupid', 'bitch', 'hell', 'burn']
for word in list:
    synset = wordnet.synsets(word)
    for syn in synset:
        for lemma in syn.lemmas():
            if lemma.name() not in syns_list and lemma.name() not in list:
                syns_list.append(lemma.name())
list += syns_list

tem = []
for i in range(len(twitts)):
    tokenize_twi = nltk.word_tokenize(twitts.loc[i, 'text'].lower())
    if find_contain_set(list, tokenize_twi):
        tem.append(i)

with open("/Users/Vanmir/Desktop/test.json", 'w') as f:
    f.write(json.dumps(total_counts))

with open("/Users/Vanmir/Desktop/test2.json", 'w') as f:
    f.write(json.dumps(dict2))
