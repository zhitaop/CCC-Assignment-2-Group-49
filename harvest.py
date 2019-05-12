import tweepy
import json
import connect
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import setting
from setting import *
import _thread


user_set = set()

class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        screen_name = data['user']['screen_name']
        #print("Streaming API recieve: " + screen_name)

        #network_list = dig_friend(screen_name)
        check_user(screen_name)

        if data['in_reply_to_screen_name']:
            reply_name = data['in_reply_to_screen_name']
            '''if reply_name not in network_list:
                network_list.append(reply_name)'''
        
            check_user(reply_name)
        #check_list(network_list)
        
        return True
    

'''
def dig_friend(screen_name):
    friends = [screen_name]
    try:
        #Lu2
        friend_ck = 'pzbMllfHPgKnKP8F8y6CXqrM6'
        friend_cs = 'va1IxRVmE4kVRIvhXyiIGryK5QJ7XXhMzKPSBYz2YE1mG2wymG'
        friend_at = '1127478273984700418-ztAaCxAmDzToVuUsRtXT6XEIlnA8I5'
        friend_as = 'ezJ5l9QGSatNhYSBpZVwE3FtCGSZaVA4XtKdCWc6TwYvc'

        friend_auth = OAuthHandler(friend_ck, friend_cs)
        friend_auth.set_access_token(friend_at, friend_as)
        friend_api = tweepy.API(friend_auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

        for friend in tweepy.Cursor(friend_api.friends, id = screen_name).items(5):
            friends.append(friend.screen_name)
        
        print(str(len(friends) - 1) + " friends from " + screen_name)
    except tweepy.error.RateLimitError as e:
        pass

    return friends
    '''

def check_user(screen_name):
    if screen_name not in user_set:
        user_set.add(screen_name)
        length = len(user_set)
        index = (length + len(AUTH_LIST) - 1) % len(AUTH_LIST)
        print("New screen_name: " + screen_name)
        
        try:
            _thread.start_new_thread(read_user, (screen_name, index, ))
        except Exception as e:
            print("Restful API Index " + str(index) + e)

'''
def check_list(network_list):
    for screen_name in network_list:
        if screen_name not in user_set:
            user_set.add(screen_name)
            length = len(user_set)
            index = (length + len(Auth_list) - 1) % len(Auth_list)
            print("New screen_name: " + screen_name)
        
            try:
                _thread.start_new_thread(read_user, (screen_name, index, ))
            except Exception as e:
                print("Restful API Index " + str(index) + e)
'''

def read_user(screen_name, index):

    rest_auth = OAuthHandler(AUTH_LIST[index]['rest_ck'], AUTH_LIST[index]['rest_cs'])
    rest_auth.set_access_token(AUTH_LIST[index]['rest_at'], AUTH_LIST[index]['rest_as'])
    rest_api = tweepy.API(rest_auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

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

if __name__ == '__main__':
    stream_auth = OAuthHandler(STREAMING_AUTH['c_k'], STREAMING_AUTH['c_s'])
    stream_auth.set_access_token(STREAMING_AUTH['a_t'], STREAMING_AUTH['a_s'])
    stream_api = tweepy.API(stream_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    streamListener = TwitterStreamListener()
    my_stream = Stream(auth = stream_api.auth, listener = streamListener)
    my_stream.filter(locations = VIC_BOX)


