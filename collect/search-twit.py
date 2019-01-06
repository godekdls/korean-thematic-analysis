import json
from dateutil.parser import parse
from dateutil.relativedelta import *
import twitter

# https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search#CountsEndpoint
# billing TT
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

# print(api.VerifyCredentials())

with open('./data/movie1.json', encoding="utf-8") as data_file:
    movie = json.load(data_file)

# print(movie["title"])
release_data = '2019-01-02'#movie["release_date"]
before = (parse(release_data) + relativedelta(months=-1)).strftime("%Y-%m-%d")

search = api.GetSearch(term=movie["title"], until=release_data, since=before, lang='ko', result_type="mixed",
                       include_entities=True, return_json=False, count=100)

print(search)
print(len(search))