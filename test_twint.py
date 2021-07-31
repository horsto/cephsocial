from pathlib import Path
import datetime
import twint


output_json = Path('test.json')
try:    
    output_json.unlink()
except FileNotFoundError:
    pass 


c = twint.Config()

c.Media = True

# Define search and exclude some users
c.Search = '"octopus" OR "cephalopod" AND "research" OR "science" OR "scientific" -filter:replies\
             -from:oct_network -from:science_octopus -@science_octopus'
c.Lang = 'en'
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