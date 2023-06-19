import tweepy
import time

auth = tweepy.OAuth1UserHandler(
    consumer_key='dB5olcSqt4kFs8PWBOjewSeHH',
    consumer_secret='ANXUAZdWwIZ52227d39d5fjZGopQ46XwWGehG0MQsmefRa2Xpq',
    access_token='756634151642595329-lytDEE7J08OSWlsbWbS7IQpnQbqaAQi',
    access_token_secret='bl1Fb549QrXVhjlBkCI9EtPixdeLEnPzwBJpP8unaKJyr'
)
api = tweepy.API(auth)

# How do you say "Ukraine/Ukrainian migrant" in Polish?
# English, Ukrainian, Polish, Russian
query_list = "Ukraine OR " \
             "Ukrainian OR " \
             "(Ukraine Refugee) OR " \
             "(Ukrainian Refugee) OR " \
             "(Ukraine Migrant) OR " \
             "(Ukrainian Migrant) OR " \
             "Україна OR " \
             "українська OR " \
             "(Україна Біженець) OR " \
             "(українська Біженець) OR " \
             "(Україна Мігрант) OR " \
             "(українська Мігрант) OR " \
             "Ukraina OR " \
             "ukraiński OR " \
             "(Ukraina Uchodźca) OR " \
             "(ukraiński Uchodźca) OR " \
             "Украина OR " \
             "украинец OR " \
             "(Украина беженец) OR " \
             "(украинец беженец) OR " \
             "(Украина мигрант) OR " \
             "(украинец мигрант)"


def get_tweets(lastID):
    count = 3  # rate limit = 15
    command = api.search_tweets
    query = query_list + " -filter:retweets -filter:replies"
    tweets = [tweet for tweet in tweepy.Cursor(command,
                                               q=query,
                                               result_type='recent',
                                               since_id=lastID,
                                               count=count).items(count)]
    for tweet in tweets:
        print(tweet.text + '\n' + '-' * 100 + '\n')

    time.sleep(10)  # seconds
    get_tweets(tweets[count-1].id)  # Recursively call function /w last tracked ID


get_tweets(0)  # Initiate function call

