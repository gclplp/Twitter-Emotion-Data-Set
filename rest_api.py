import tweepy
from timeit import default_timer as timer
from tweepy import OAuthHandler
from pymongo import MongoClient
import twitter_credentials

start = timer()

"Setting up authoristion keys NOT included here"
auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

"Setting up mongoDB"
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterdb']

"Hashtag for each of the motions I selected"
emotions = ["#angry", "#happy", "#excited", "#trust", "#sadness", "#scared"]

"loop over the list of emotions and put them in corresponding collection, 450 tweets no retweets"
for word in emotions:
    for tweet in tweepy.Cursor(api.search,q=word + " -filter:retweets", lang="en",count = 100, tweet_mode = "extended").items(450):
        print(tweet._json)
        db[word].insert(tweet._json)
total_time = timer() - start
print(total_time)