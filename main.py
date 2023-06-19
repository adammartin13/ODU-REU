import tweepy
import logging
import time

logger = logging.getLogger("tweepy")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="tweepy.log")
logger.addHandler(handler)

auth = tweepy.OAuth1UserHandler(
    consumer_key='dB5olcSqt4kFs8PWBOjewSeHH',
    consumer_secret='ANXUAZdWwIZ52227d39d5fjZGopQ46XwWGehG0MQsmefRa2Xpq',
    access_token='756634151642595329-lytDEE7J08OSWlsbWbS7IQpnQbqaAQi',
    access_token_secret='bl1Fb549QrXVhjlBkCI9EtPixdeLEnPzwBJpP8unaKJyr'
)
api = tweepy.API(auth)

# GET rate limit for basic accounts is 15 per 15 minutes
# GET rate limit for research accounts is 300 per 15 minutes
# A Tweet ID is the string of numbers at the end of a tweet URL

# Basic search commands
# q = query string, max character count 500
# include_ext_edit_control = true/false, determines if tweet edit metadata is returned. Default false.
# geocode = Returns tweets of users within a specified geocode
# lang = Specify language
# result_type = mixed/recent/popular. Determines which type of result is desired.
# count = number of tweets to return
# until = YYYY-MM-DD. Returns tweets before the given date.
# since_id = Returns results with an ID more recent than that which is provided.
# max_id = Returns results with an ID older than that which is provided.

# Basic Search
# Search arguments are comma-separated in the Cursor parameters.
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''
# Retweets can be filtered out via the '-filter:retweets' argument in the query
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine -filter:retweets"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''
# Replies can be filtered via '-filter:replies' in the query
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine -filter:retweets -filter:replies"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''

# Logical searches
# Advanced operators are available to accounts with Academic Research access
# Searching for results with 'Ukraine' AND 'Refugee' is default via space-separated variables
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine Refugee -filter:retweets -filter:replies"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''
# Searching for results with 'Ukraine' OR 'Poland' is done via the 'OR' operator
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine OR Poland -filter:retweets -filter:replies"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''
# Searching for results with 'Ukraine' AND NOT 'war' is done via the negation '-' operator
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "Ukraine -war -filter:retweets -filter:replies"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''
# Search logic can be grouped with parenthesis: 'Ukraine' AND 'war' but NOT 'Poland' and 'war'
# DOES NOT WORK, returns error 32. Not sure why, will fix if needed.
'''
count = 5  # rate limit = 15
command = api.search_tweets
query = "(Ukraine war) OR (Poland -war) -filter:retweets -filter:replies"
tweets = [tweet for tweet in tweepy.Cursor(command,
                                           q=query,
                                           result_type='recent',
                                           count=count).items(count)]
for tweet in tweets:
    print(tweet.text + '\n' + '-' * 100 + '\n')
'''

# Looping
# The below code will generate a tweet containing "Ukraine" ten seconds
'''
def get_tweets():
    count = 1  # rate limit = 15
    command = api.search_tweets
    query = "Ukraine -filter:retweets -filter:replies"
    tweets = [tweet for tweet in tweepy.Cursor(command,
                                               q=query,
                                               result_type='recent',
                                               count=count).items(count)]
    for tweet in tweets:
        print(tweet.text + '\n' + '-' * 100 + '\n')

    time.sleep(10)
    get_tweets()


get_tweets()
'''

# The below code will store the last tweet ID queried and ensure that all new tweets are newer than it.


def get_tweets(lastID):
    count = 3  # rate limit = 15
    command = api.search_tweets
    query = "Ukraine -filter:retweets -filter:replies"
    tweets = [tweet for tweet in tweepy.Cursor(command,
                                               q=query,
                                               result_type='recent',
                                               since_id=lastID,
                                               count=count).items(count)]
    for tweet in tweets:
        print(tweet.text + '\n' + '-' * 100 + '\n')

    print(tweets[count - 1].id)
    time.sleep(10)  # seconds
    get_tweets(tweets[count-1].id)  # Recursively call function /w last tracked ID


get_tweets(0)  # Initiate function call
