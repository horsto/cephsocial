from fastapi import FastAPI
from importlib_metadata import PackageNotFoundError
import datetime 

app = FastAPI()

TWINT_ERROR = None
try:
    import twint
    HAS_TWINT = True
except BaseException as e:
    HAS_TWINT = False
    TWINT_ERROR = e


############ GENERAL SETTINGS #########################################################################
# Filter key words in tweets 
filter_keys = ['art',
            'design',
            'dance',
            'soup',
            'hair',
            'cuisine',
            'menu',
            'grill',
            'eat',
            'ate',
            'cook',
            'bowl',
            'fried',
            'stock',
            'statue',
            'plush',
            'gift',
            ]
            


############ HELPERS ##################################################################################

def filter_transcribe_tweets(tweets, filter_language=None):
    '''
    Filter tweets by language and key words.
    Transcribe essentials only. 
    filter_language : string : e.g. "en", default: None

    
    '''
    
    #Transscribe essentials only
    all_tweets = {}
    for tweet in tweets:
        # Filter lang
        if (filter_language is not None) and (tweet.lang != filter_language): 
            continue 

        skip = False
        for key in filter_keys:
            if key in tweet.tweet.lower():
                skip = True
        if skip: 
            continue 

        tweet_dict = {
            'datetime' : tweet.datetime,
            'username' : tweet.username,
            'name'     : tweet.name,
            'place'    : tweet.place,
            'photos'   : tweet.photos,
            'tweet'    : tweet.tweet,
            'likes'    : tweet.likes_count,
            'near'     : tweet.near,
            'geo'      : tweet.geo,
            'link'     : tweet.link,
        }
        all_tweets[tweet.id] = tweet_dict

    return all_tweets 

############ API ######################################################################################

@app.get("/")
def read_root():
    return 'This is the octo fastAPI. Welcome!'

@app.get("/check_twint")
def twint_status():
    if HAS_TWINT: 
        return f'Twint found! {twint.__version__} | {twint.__file__}'
    else:
        return f'Twint not found. {TWINT_ERROR}'

@app.get("/tweets/tomopteris")
def get_tomopteris_tweets():
    c = twint.Config()
    
    c.Media = True
    c.Search = 'tomopteris -filter:replies -from:tomopteris -@tomopteris'
    c.Lang = 'en'
    c.Show_hashtags = True
    last_week  =  datetime.datetime.now() - datetime.timedelta(days=21)
    c.Since = datetime.datetime.strftime(last_week, "%Y-%m-%d")
    c.Min_likes = 1
    c.Filter_retweets = True
    c.Store_object = True

    # Run search
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    all_tweets = filter_transcribe_tweets(tweets, filter_language='en')
    twint.output.clean_lists()
    return all_tweets

@app.get("/tweets/octo")
def get_octo_tweets():
    c = twint.Config()
 
    c.Media = True

    # Define search and exclude some users
    c.Search = '"octopus" AND "research" OR "science" -filter:replies -from:oct_network'
    c.Show_hashtags = True
    last_week  =  datetime.datetime.now() - datetime.timedelta(days=21)
    c.Since = datetime.datetime.strftime(last_week, "%Y-%m-%d")
    c.Min_likes = 1
    c.Lang = 'en'
    c.Filter_retweets = True
    c.Store_object = True
    
    # Run search
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    all_tweets = filter_transcribe_tweets(tweets, filter_language='en')
    twint.output.clean_lists()
    return all_tweets