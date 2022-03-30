import json
import tweepy
from kafka import KafkaProducer

consumer_key = 'Y9si3VOIlko4W9SsBQNl7gpNY'
consumer_secret = 'cr892ET3ZYXMiXlZ1y2TvpymcDY625rbYklbBeoxvL9mD4MwmO'
access_token = '867110384431509510-iaX6o8unBJUTAxdbdOPmMuG3TECvM2L'
access_secret = 'ge3vG38ybphk3GMt1vXnt3kZ3RnoCk5jDTbEqraSUkPhg'


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='nc-de-vm-v3',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.tweets = []

    def on_data(self, data):
        # data is the full *tweet* json data
        api_events = json.loads(data)

        # Gathring relevant values
        # Event-related values
        event_keys = ['created_at', 'id', 'text']
        twitter_events = {k: v for k, v in api_events.items()
                          if k in event_keys}
        twitter_events['tweet_created_at'] = twitter_events.pop('created_at')
        twitter_events['tweet_id'] = twitter_events.pop('id')
        # User-related values
        user_keys = ['id', 'name', 'created_at', 'location', 'url', 'protected', 'verified',
                     'followers_count', 'friends_count', 'listed_count', 'favourites_count',
                     'statuses_count', 'withheld_in_countries']
        user_events = {k: v for k, v in api_events['user'].items()
                       if k in user_keys}
        user_events['user_acount_created_at'] = user_events.pop('created_at')
        user_events['user_id'] = user_events.pop('id')

        # Marge dictioneries
        user_events.update(twitter_events)
        events = user_events

        # send data to kafka topic(s)
        self.producer.send('TweeterArchive', events)
        self.producer.send('TweeterData', events)
        self.producer.flush()

        print(events)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def initialize():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth=api.auth, listener=stream)
    twitter_stream.filter(track=['Trump'], languages=['en'])


initialize()