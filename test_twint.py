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
c.Search = '"octopus" AND "research" OR "science" -filter:replies -from:oct_network'
c.Lang = 'en'
c.Show_hashtags = True

last_week  =  datetime.datetime.now() - datetime.timedelta(days=7)
c.Since = datetime.datetime.strftime(last_week, "%Y-%m-%d")
c.Min_likes = 5
c.Lang = 'en'
c.Filter_retweets = True
c.Store_object = True
# Run search
twint.run.Search(c)

tweets = twint.output.tweets_list