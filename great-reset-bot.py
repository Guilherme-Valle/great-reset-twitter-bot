# coding=utf-8
import tweepy
import sys
import os
from importlib import reload


consumer_key = os.environ.get('TWITTER_API_RESET_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_API_RESET_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_API_RESET_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_API_RESET_ACCESS_TOKEN_SECRET')
logf = open("errors.log", "w")
reload(sys)
sys.setdefaultencoding('utf8')

class greatResetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, status):
        if not status.retweeted and status.user.id != self.me.id:
            try:
                status.retweet()
            except Exception as exception:
                logf.write(exception.response.text)


try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets_listener = greatResetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["Great Reset", "Grande Reset", "great reset", "grande reset", "Klaus Schwab", "Fórum econômico mundial",
                         "Você não terá nada e será feliz",
                         "Fórum econômico", "Comer insetos"], languages=["pt"])

except tweepy.TweepError as e:
    logf.write(e.response.text)
except tweepy.RateLimitError:
    logf.write("RATELIMITERROR")
