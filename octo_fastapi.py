from pathlib import Path
import twint
from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return 'This is the octo fast API. Welcome!'


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/tweets/tomopteris")
def get_tomopteris_tweets():
    c = twint.Config()

    c.Media = True
    c.Search = 'tomopteris -filter:replies -from:tomopteris -@tomopteris'
    c.Lang = 'en'
    c.Show_hashtags = True
    c.Since = '2021-06-01'
    c.Min_likes = 5
    c.Filter_retweets = True
    c.Store_object = True
    # Run search
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    #Transscribe essentials only
    all_tweets = {}
    for tweet in tweets: 
        tweet_dict = {
            'datetime' : tweet.datetime,
            'username' : tweet.username,
            'name'     : tweet.name,
            'place'    : tweet.place,
            'timezone' : tweet.timezone,
            'photos'   : tweet.photos,
            'tweet'    : tweet.tweet,
            'likes'    : tweet.likes_count,
            'near'     : tweet.near,
            'geo'      : tweet.geo,
            'link'     : tweet.link,
        }
        all_tweets[tweet.id] = tweet_dict

    return all_tweets

@app.get("/tweets/octo")
def get_octo_tweets():
    c = twint.Config()

    c.Media = True

    # Define search and exclude some users
    c.Search = '"octopus research" -filter:replies -from:spencilular\
                -from:decentricity -from:octopushermit -from:pcaketheoctopus\
                -from:shionskyplz -from:glamourpossum -from:ecooctopus -from:ochead7\
                -from:fevertheoctopus -from:http_lovecraft -from:lboherdoll -from:octopusgallery\
                -from:doodleoctopus -from:onogork -from:del_db -from:octopuscaveman -from:underthatstone1\
                -from:acetoneoctopus'
    c.Lang = 'en'
    c.Show_hashtags = True
    c.Since = '2021-06-01'
    c.Min_likes = 5
    c.Lang = 'en'
    c.Limit = 25
    c.Filter_retweets = True
    c.Store_object = True
    # Run search
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    # Filter key words in tweets 
    filter_keys = ['art',
                  'design',
                  'dance',
                  'witch',
                  'food',
                  'hair',
                  'cuisine',
                  'menu',
                  'grill',
                  'eat',
                  'ate',
                  'cook',
                  'bowl',
                  'fried',
                  'snack',
                  'toy',
                  'stock',
                  'statue',
                  'plush',
                  'gift',
                  'present'
                  ]

    #Transscribe essentials only
    all_tweets = {}
    for tweet in tweets:
        # Filter lang
        if tweet.lang != 'en': 
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
            'timezone' : tweet.timezone,
            'photos'   : tweet.photos,
            'tweet'    : tweet.tweet,
            'likes'    : tweet.likes_count,
            'near'     : tweet.near,
            'geo'      : tweet.geo,
            'link'     : tweet.link,
        }
        all_tweets[tweet.id] = tweet_dict

    return all_tweets