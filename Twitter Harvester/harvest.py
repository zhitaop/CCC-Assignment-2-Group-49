'''
Team 49
# Aijia Yang 957285
# Guojun Han 905114
# Yi Lu 917371
# Yumika Suzuki 1011143
# Zhitao Pan 844505
'''

import tweepy
import json
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import setting
from setting import *
import _thread
from process_twi import TweetProcesser
import couchdb
import create_view

user = 'zhitao'
password = 'cccgroup49'
dbname = 'twitter_data'
processed_dbname = 'twitter_processed'

user_set = set()

class TwitterStreamListener(StreamListener):

    def __init__(self):
        self.tweet_processer = TweetProcesser(user, password, processed_dbname)
        self.couchserver = couchdb.Server('http://db:5984')
        #self.couchserver = couchdb.Server(f'http://{user}:{password}@127.0.0.1:5984')
        if dbname in self.couchserver:
            self.db = self.couchserver[dbname]
        else:
            self.db = self.couchserver.create(dbname)

    def on_data(self, data):
        data = json.loads(data)
        screen_name = data['user']['screen_name']
        #print("Streaming API recieve: " + screen_name)

        #network_list = dig_friend(screen_name)
        self.check_user(screen_name)

        if data['in_reply_to_screen_name']:
            reply_name = data['in_reply_to_screen_name']
            '''if reply_name not in network_list:
                network_list.append(reply_name)'''
        
            self.check_user(reply_name)
        #check_list(network_list)
        
        return True
    
    def check_user(self, screen_name):
        if screen_name not in user_set:
            user_set.add(screen_name)
            length = len(user_set)
            index = (length + len(AUTH_LIST) - 1) % len(AUTH_LIST)
            print("New screen_name: " + screen_name)
            
            try:
                _thread.start_new_thread(self.read_user, (screen_name, index, ))
            except Exception as e:
                print("Restful API Index " + str(index) + e)


    def read_user(self, screen_name, index):

        rest_auth = OAuthHandler(AUTH_LIST[index]['rest_ck'], AUTH_LIST[index]['rest_cs'])
        rest_auth.set_access_token(AUTH_LIST[index]['rest_at'], AUTH_LIST[index]['rest_as'])
        rest_api = tweepy.API(rest_auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

        start = datetime.datetime.now()
        count = 0
        #file_name = screen_name + '.json'
        for status in tweepy.Cursor(rest_api.user_timeline, id = screen_name, tweet_mode = 'extended', lang = 'en').items(300):
            if status.coordinates or status.place:
                count += 1

                json_obj = status._json
                json_obj['_id'] = str(json_obj['id'])
                try:
                    self.db.save(json_obj)
                except couchdb.http.ResourceConflict as error:
                    print(error)
                self.tweet_processer.process_tweet(json_obj)
                #f.write(json.dumps(status._json)+'\n')
        
        end = datetime.datetime.now()
        print("Index " + str(index) + " Download " + str(count) + " from " + screen_name + " in " + str(end - start))

if __name__ == '__main__':
    stream_auth = OAuthHandler(STREAMING_AUTH['c_k'], STREAMING_AUTH['c_s'])
    stream_auth.set_access_token(STREAMING_AUTH['a_t'], STREAMING_AUTH['a_s'])
    stream_api = tweepy.API(stream_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    streamListener = TwitterStreamListener()
    my_stream = Stream(auth = stream_api.auth, listener = streamListener)
    my_stream.filter(locations = VIC_BOX)
