import tweepy
import json
import connect
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import _thread


user_set = set()
Auth_list = [
    #index = 0, Lu1
    {
        'rest_ck' : 'A5KRagrcPWbwUF7UkguySO5au',
        'rest_cs' : 'yfKVPUWHrrtVmwvBzrGecZvBvISQwZ48xNkgvfweN8dYt3lmES',
        'rest_at' : '1126754709421715458-Ttxz0zua58zI9EIAAVEuXgmX6c0m2F',
        'rest_as' : 'PHQ1CZBLPP5xHNHr8Uvt0mLpzUrgoqojDJcc2Z6j5tHJi'
    },
    #index = 1, Han1
    {
        'rest_ck' : 'A5KRagrcPWbwUF7UkguySO5au',
        'rest_cs' : 'yfKVPUWHrrtVmwvBzrGecZvBvISQwZ48xNkgvfweN8dYt3lmES',
        'rest_at' : '1126754709421715458-Ttxz0zua58zI9EIAAVEuXgmX6c0m2F',
        'rest_as' : 'PHQ1CZBLPP5xHNHr8Uvt0mLpzUrgoqojDJcc2Z6j5tHJi'
    },
    #index = 2, Pan1
    {
        'rest_ck' : 'Sds1H0cEaS7Vcg3UKgNJgXmjP',
        'rest_cs' : 'YQBjCfutKAEt1bfSiHbTXigPSyebFhg229t7UMJnQWMrbk1i0t',
        'rest_at' : '1059274882830090240-hwuhl4Ur2TmXTQjhZqEW0MGARyhRAo',
        'rest_as' : 'TBraXyUXTIbEGUMqvsULAmyPqqVuyrRoekEVo8mZuqQkG'
    },
    #index = 3, Zhang1
    {
        'rest_ck' : 'y0iZXfr8ZDCi9tmSlNZ33NPTa',
        'rest_cs' : 'BhBLtViYSG1v6RCyzVQ5h2epfgPx7vrQ4lALW4L6QZFSs7cj1i',
        'rest_at' : '987483594338717697-7SwKfgTD1H3YCKCPVxtvuGMS88n0zMX',
        'rest_as' : 'P9qdrdcMIdnM6BoP8n9cFndPd2B8y3dCpRH36GCBUlRC7'
    }
]

class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        screen_name = data['user']['screen_name']
        check_user(screen_name)

        if data['in_reply_to_screen_name']:
            reply_name = data['in_reply_to_screen_name']
            check_user(reply_name)
        
        return True

def check_user(screen_name):
    if screen_name not in user_set:
        user_set.add(screen_name)
        length = len(user_set)
        index = (length + len(Auth_list) - 1) % len(Auth_list)
        print("New screen_name: " + screen_name)
    
        try:
            _thread.start_new_thread(read_user, (screen_name, index, ))
        except Exception as e:
            print(e)

def read_user(screen_name, index):
    '''
    #ly
    rest_ck = 'A5KRagrcPWbwUF7UkguySO5au'
    rest_cs = 'yfKVPUWHrrtVmwvBzrGecZvBvISQwZ48xNkgvfweN8dYt3lmES'
    rest_at = '1126754709421715458-Ttxz0zua58zI9EIAAVEuXgmX6c0m2F'
    rest_as = 'PHQ1CZBLPP5xHNHr8Uvt0mLpzUrgoqojDJcc2Z6j5tHJi'
    '''

    rest_auth = OAuthHandler(Auth_list[index]['rest_ck'], Auth_list[index]['rest_cs'])
    rest_auth.set_access_token(Auth_list[index]['rest_at'], Auth_list[index]['rest_as'])
    rest_api = tweepy.API(rest_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    start = datetime.datetime.now()
    count = 0
    #file_name = screen_name + '.json'
    with open('test-4thread.json', 'a', encoding = 'utf-8') as f:
        for status in tweepy.Cursor(rest_api.user_timeline, id = screen_name, tweet_mode = 'extended', lang = 'en').items(300):
            if status.coordinates or status.place:
                count += 1
                f.write(json.dumps(status._json)+'\n')
    
    end = datetime.datetime.now()
    print("Index " + str(index) + " Download " + str(count) + " from " + screen_name + " in " + str(end - start))

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


