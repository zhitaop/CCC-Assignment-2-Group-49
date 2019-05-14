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

class TweetProcesser:

    def __init__(self, db_user, db_pw, processed_db_name):
        self.couchserver = couchdb.Server('http://127.0.0.1:5984')
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


    def read_twi_coors__2(self, record):
        coordinate = record['coordinates']
        place = record['place']
        if coordinate:
            return coordinate['coordinates']
        elif place:
            coordinate = record['place']['bounding_box']['coordinates'][0][0]
            return coordinate
        return None

    def read_twi_coors(self, record):
        coordinate = record['coordinates']
        if coordinate:
            return coordinate['coordinates']
        elif record['place']:
            # if place == 'Melbourne, melbourne's coordinate is assigned
            if record['place']['id'] == '01864a8a64df9dc4':
                coordinate = [144.96332, -37.814]
                return coordinate
            else:
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
