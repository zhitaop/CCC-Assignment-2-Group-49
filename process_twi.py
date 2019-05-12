import json
import re
import nltk
from shapely.geometry import shape, Point
from nltk.corpus import wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# read file
with open("/Users/Vanmir/Desktop/vic_lga.json", 'r') as file:
    line = file.readline()
    vic_lga = json.loads(line)

# twitter info
twitterfile1 = "/Users/Vanmir/Desktop/largetest.json"


def preprocess_twi(twi_text):
    # remove hyperlink
    twi_text = re.sub(r'http\S+', '', twi_text)
    # remove html entities &amp
    twi_text = re.sub(r'\&\w*;', '', twi_text)
    # remove @user
    twi_text = re.sub('@[^\s]+', '', twi_text)
    # remove hashtag symbol '#'
    twi_text = re.sub('#', ' ', twi_text)
    #remove punctuation including '.'
    twi_text = re.sub('\.', ' ', twi_text)
    return twi_text


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


def create_key_word_set(word_set):
    syns_list = []
    for word in word_set:
        synset = wordnet.synsets(word)
        for syn in synset:
            for lemma in syn.lemmas():
                if lemma.name() not in syns_list and lemma.name() not in word_set:
                    syns_list.append(lemma.name())
    word_set += syns_list
    return word_set


def find_contain_set(wrath_set, twi_set):
    contain_set = [word for word in wrath_set if word in twi_set]
    if contain_set:
        return True
    else:
        return False


list_temp = ['hate', 'angry', 'offended', 'frustrating', 'snap', 'pissed',
             'irritated', 'shit', 'shitty', 'resentful', 'mad', 'furious', 'foolish',
             'stupid', 'rage', 'foolish', 'bitch', 'hell', 'burn']

final_list = create_key_word_set(list_temp)

# read one twitter info
line = line.strip(',\n')
record = json.loads(line)
text_info = {}
# dict3 = {}
lga_area = find_lga_area(vic_lga, record)
if lga_area is not False:
    text = record['text']
    text = preprocess_twi(text)

    text_info['id'] = record['id']
    text_info['text'] = text
    text_info['lga_area'] = lga_area
    text_info['coordinates'] = read_twi_coors(record)

    #sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)['compound']
    text_info['sentiment_score'] = score

    # if the text contains the key words, it will be used to count
    text_norm = nltk.word_tokenize(text.lower())
    if find_contain_set(final_list, text_norm):
        if_key_words = 'yes'
    else:
        if_key_words = 'no'
    text_info['key_words'] = if_key_words
else:


#couchdb.save(text_info)
