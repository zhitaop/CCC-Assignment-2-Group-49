"""
Team 49
# Aijia Yang 957285
# Guojun Han 905114
# Yi Lu 917371
# Yumika Suzuki 1011143
# Zhitao Pan 844505
"""

import json
import re
import nltk
from shapely.geometry import shape, Point
from nltk.corpus import wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import couchdb
import create_view
import numpy as np
import os
import random

lga_coordinates = [
    [144.9436708724537, -37.81071454646296],  # Melbourne
    [144.9660383582063, -37.85220035716027],  # Port Phillip
    [145.033638640678,- 37.85795059419824],  # Stonnington
    [144.9985270648188, -37.80226806140895],  # Yarra
    [145.0851374567692, -37.73037084082312],  # Banyule
    [145.0179708456197, -37.94168038210734],  # Bayside
    [145.063093351917, -37.819292999541],  # Boroondara
    [144.8033088163138, -37.7475527857568],  # Brimbank
    [145.0143361006927, -37.73346198925955],  # Darebin
    [145.0426027099654, -37.90120587623827],  # Glen Eira
    [144.8300263113892, -37.8546890641181],  # Hobsons Bay
    [145.1051027642337, -37.98866932623822],  # Kingston
    [145.1885678960027, -37.76158520614524],  # Manningham
    [144.8777693651151, -37.79527966838285],  # Maribyrnong
    [145.1440336768838, -37.89714304214255],  # Monash
    [144.8957591954861, -37.74952121591947],  # Moonee Valley
    [144.9488194951094, -37.72984049212152],  # Moreland
    [145.1550568018552, -37.83024801561037],  # Whitehorse
    [145.572664776398, -38.08305303754749],  # Shire of Cardinia
    [145.3092984633363, -38.10028048292309],  # Casey
    [145.1737366635034, -38.13466424895159],  # Frankston
    [145.1900119338524, -38.00565130989552],  # Greater Dandenong
    [144.824627290565, -37.58916543350263],  # Hume
    [145.2586574542673, -37.88896083357653],  # Knox
    [145.265259897546, -37.80486733918201],  # Maroondah
    [144.6260213945261, -37.69295990975532],  # Melton
    [145.0354047970413, -38.34194215786155],  # Shire of Mornington Peninsula
    [145.2368568178074, -37.62289507918575],  # Shire of Nillumbik
    [145.0776840855983, -37.54719935448867],  # Whittlesea
    [144.6182493677213, -37.88665897514785],  # Wyndham
    [145.6969471178653, -37.71425616183905]  # Shire of Yarra Ranges
]

lga_population = [
    135959,  # Melbourne
    100863,  # Port Phillip
    103832,  # Stonnington
    86657,  # Yarra
    121865,  # Banyule
    97087,  # Bayside
    167231,  # Boroondara
    194319,  # Brimbank
    146719,  # Darebin
    140875,  # Glen Eira
    88778,  # Hobsons Bay
    151389,  # Kingston
    116255,  # Manningham
    82288,  # Maribyrnong
    182618,  # Monash
    116671,  # Moonee Valley
    162558,  # Moreland
    162078,  # Whitehorse
    94128,  # Shire of Cardinia
    299301,  # Casey
    134143,  # Frankston
    152050,  # Greater Dandenong
    194376,  # Hume
    154110,  # Knox
    110376,  # Maroondah
    135443,  # Melton
    154999,  # Shire of Mornington Peninsula
    61273,  # Shire of Nillumbik
    197491,  # Whittlesea
    217122,  # Wyndham
    149537  # Shire of Yarra Ranges
]

total_population = 0
for num in lga_population:
    total_population += num

lga_prob = []
for num in lga_population:
    lga_prob.append(num / float(total_population))

class TweetProcesser:

    def __init__(self, db_user, db_pw, processed_db_name):
        self.couchserver = couchdb.Server('http://db:5984')
        #self.couchserver = couchdb.Server(f'http://{db_user}:{db_pw}@127.0.0.1:5984')
        if processed_db_name in self.couchserver:
            self.processed_db = self.couchserver[processed_db_name]
        else:
            self.processed_db = self.couchserver.create(processed_db_name)

        create_view.create_view(self.processed_db, 'negative', 'negative_score.js', '_count' )
        create_view.create_view(self.processed_db, 'wrath', 'wrath_tweets.js', '_count' )
        create_view.create_view(self.processed_db, 'sentiment', 'sentiment.js', '_count' )

        # read file
        vic_lga_dir = os.path.dirname(os.path.realpath(__file__))+"/vic_lga.json"
        with open(vic_lga_dir, 'r') as file:
            line = file.readline()
            self.vic_lga = json.loads(line)

    def preprocess_twi(self, twi_text):
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

    def read_twi_coors(self, record):
        coordinate = record['coordinates']
        if coordinate:
            return coordinate['coordinates']
        elif record['place']:
            # if place == 'Melbourne, melbourne's coordinate is assigned
            if record['place']['id'] == '01864a8a64df9dc4':
                coordinate = random.choices(population=lga_coordinates, weights=lga_prob, k=1)[0]
                return coordinate
            elif record['place']['bounding_box']:
                coor_list = record['place']['bounding_box']['coordinates'][0]
                coordinate = np.sum([coor_list[0], coor_list[1], coor_list[2], coor_list[3]], axis=0) / 4
                return coordinate.tolist()
        return None


    def find_lga_area(self, lga_info, record):
        coordinate = self.read_twi_coors(record)
        if coordinate:
            lga_geo = lga_info['features']
            for coor in lga_geo:
                if Point(coordinate).within(shape(coor['geometry'])):
                    return coor['properties']['vic_lga__3']
        return False

    
    def process_tweet(self, tweet):
        record = tweet
        # read one twitter info
        #line = line.strip(',\n')
        #record = json.loads(line)
        text_info = {}
        # dict3 = {}
        lga_area = self.find_lga_area(self.vic_lga, record)
        if lga_area is not False:
            if record.get('text') == None:
                text = record['full_text']
            else:
                text = record['text']

            text = self.preprocess_twi(text)

            text_info['_id'] = record['_id']
            text_info['text'] = text
            text_info['lga_area'] = lga_area
            text_info['coordinates'] = self.read_twi_coors(record)

            #sentiment analysis
            analyzer = SentimentIntensityAnalyzer()
            score = analyzer.polarity_scores(text)['compound']
            text_info['sentiment_score'] = score

            '''
            # if the text contains the key words, it will be used to count
            text_norm = nltk.word_tokenize(text.lower())
            if find_contain_set(final_list, text_norm):
                if_key_words = 'yes'
            else:
                if_key_words = 'no'
            text_info['key_words'] = if_key_words
            '''

            print(text_info['_id'])
            try:
                self.processed_db.save(text_info)
            except couchdb.http.ResourceConflict as error:
                print(error)


# total_count, twitter_count_in_vic, wrath total count, negative total count
# score <= -0.5 (lga_count, coordinates) wrath, score <= -0.05 => negative,
