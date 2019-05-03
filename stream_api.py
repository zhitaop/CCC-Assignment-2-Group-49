import tweepy
import socket
import requests
import time
import jsonpickle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from authentication import authentication  # Consumer and access token/key

#This is a basic listener that just prints received tweets to stdout.
class TwitterStreamListener(StreamListener):

	def on_data(self, data):
		print(data)
		return True

	'''def on_status(self, status):
		get_tweet(status)
		get_user_informations(status)'''

	# Twitter error list : https://dev.twitter.com/overview/api/response-codes
	
	def on_error(self, status_code):
		if status_code == 403:
			print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
			return False


def get_tweet(tweet):
	print("Tweet Message : " + tweet.text)
	print("Tweet Favorited \t:" + str(tweet.favorited))
	print("Tweet Favorited count \t:" + str(tweet.favorite_count))
	
	# Display sender and mentions user
	if hasattr(tweet, 'retweeted_status'):
		print("Tweet send by : " + tweet.retweeted_status.user.screen_name)
		print("Original tweet ID" + tweet.retweeted_status.id_str)
		
		for screenname in tweet.retweeted_status.entities['user_mentions']:
			print("Mention user: " + str(screenname['screen_name']))
		

def get_user_informations(tweet):

	print("User ID \t:" + str(tweet.user.id))
	print("User image profil \t:" + tweet.user.profile_image_url_https)
	print("User Name \t:" + tweet.user.name)
	print("User URL \t:", tweet.user.url)
	print("User profil text color \t:" + tweet.user.profile_text_color)
	print("User background image url \t:" + tweet.user.profile_background_image_url)
	print("User Friends count \t:" + str(tweet.user.friends_count))
	print("User Screen name \t:" + tweet.user.screen_name)
	print("User Verified \t:" + str(tweet.user.verified))
	print("User Favorite count \t:" + str(tweet.user.favourites_count))
	
	if hasattr(tweet.user, 'time_zone'):
	    print("User Time zone \t:", tweet.user.time_zone)
	    print("User UTC Offset \t:" + str(tweet.user.utc_offset))
	print("User Status count \t:" + str(tweet.user.statuses_count))
	
	print("User Description \t:", tweet.user.description)
	print("User Follower count \t:" + str(tweet.user.followers_count))
    #print("User Created at \t:" + str(tweet.user.created_at))

if __name__ == '__main__':
	
	# Get access and key from another class
	auth = authentication()

	consumer_key = auth.getconsumer_key()
	consumer_secret = auth.getconsumer_secret()

	access_token = auth.getaccess_token()
	access_token_secret = auth.getaccess_token_secret()

	# Authentication
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.secure = True
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

	#Streaming API
	'''streamListener = TwitterStreamListener()
	myStream = Stream(auth=api.auth, listener=streamListener)

	myStream.filter(track=['drunk', 'liquor', 'alcohol', 'whiskey', 'vodka', 'rum'],
		locations = [144.7, -38.1, 145.45, -37.5], languages=['en'])'''

	#REST API
	searchQuery = '#melbourne'
	maxTweets = 10000
	tweetsPerQry = 100
	outputFile = 'tweets.json'

	sinceId = None
	maxId = -1

	tweetCount = 0
	print("Start downloading. Max: {0}".format(maxTweets, ","))
	with open(outputFile, 'w') as f:
		while tweetCount < maxTweets:
			try:
				if (maxId <= 0):
					if (not sinceId):
						new_tweets = api.search(q = searchQuery, count = tweetsPerQry)
					else:
						new_tweets = api.search(q = searchQuery, count = tweetsPerQry, 
							sinec_id = sinceId)
				else:
					if (not sinceId):
						new_tweets = api.search(q = searchQuery, count = tweetsPerQry, 
							max_id = str(maxId - 1))
					else:
						new_tweets = api.search(q = searchQuery, count = tweetsPerQry, 
							sinec_id = sinceId, max_id = str(maxId - 1))
				
				if not new_tweets:
					print("No more tweets found")
					break
				
				for tweet in new_tweets:
					f.write(jsonpickle.encode(tweet._json, unpicklable = False) + '\n')
				
				tweetCount += len(new_tweets)
				print("Successfully download {0} tweets".format(tweetCount, ","))
				max_id = new_tweets[-1].id
			except tweepy.TweepError as e:
				print("Some error: " + str(e))
				break
	print("In total we download {0} tweets and save to {1}".format(tweetCount, outputFile))