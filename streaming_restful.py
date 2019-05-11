import tweepy
import json
import connect
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import _thread

'''#unfinish
def clean_data(data):
    tweet_id = data['id_str']

    try:
        cleaned_data = {
            'id': data['id_str'],
            'createdAt': data['created_at'],
            'text': data['text'],
            'user': {
                'id': data['user']['id_str'],
                'name': data['user']['name'] if data['user']['name'] else None



            }
        }'''

user_set = set()

class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        screen_name = data['user']['screen_name']
        if screen_name not in user_set:
            user_set.add(screen_name)
            print("New screen_name: " + screen_name)

            try:
                _thread.start_new_thread(read_user, (screen_name,))
            except Exception as e:
                print(e)
            #read_user(screen_name)
        '''if data['coordinates'] or data['place']:
            tweet_id = data['id_str']
            #cleaned_data = clean_data(data)'''
        
        return True

def read_user(screen_name):
    #ly
    rest_ck = 'A5KRagrcPWbwUF7UkguySO5au'
    rest_cs = 'yfKVPUWHrrtVmwvBzrGecZvBvISQwZ48xNkgvfweN8dYt3lmES'
    rest_at = '1126754709421715458-Ttxz0zua58zI9EIAAVEuXgmX6c0m2F'
    rest_as = 'PHQ1CZBLPP5xHNHr8Uvt0mLpzUrgoqojDJcc2Z6j5tHJi'

    rest_auth = OAuthHandler(rest_ck, rest_cs)
    rest_auth.set_access_token(rest_at, rest_as)
    rest_api = tweepy.API(rest_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    #file_name = screen_name + '.json'
    with open('test.json', 'a', encoding = 'utf-8') as f:
        for status in tweepy.Cursor(rest_api.user_timeline, id = screen_name).items():
            if status.coordinates or status.place:
                f.write(json.dumps(status._json)+'\n')

#yaj
c_k = 'YUUejarJDZo5vFIUcU0jyNPck'
c_s = 'TPFJyMMj4oF4TBdxyurBUQdEly0Cq7j8AR5yKyfhjNZvj5vcMb'
a_t = '885237433-NBxPYyvZXRPZMLyKGtWwOmgnSfIHzd6H8Y18gwAN'
a_s = 'Llfml16Lc4X8rvXusKmt6sAfakvHM3jc65RkD2XylwOF3'
stream_auth = OAuthHandler(c_k, c_s)
stream_auth.set_access_token(a_t, a_s)
stream_api = tweepy.API(stream_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

streamListener = TwitterStreamListener()
my_stream = Stream(auth = stream_api.auth, listener = streamListener)
my_stream.filter(locations=[140.96,-39.2,150.03,-33.98])


