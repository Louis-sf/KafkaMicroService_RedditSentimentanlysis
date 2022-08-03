import json
import praw
import requests
from prawcore import NotFound

# ###############PSAW CONFIG########################
keyfile = open('secrets/prawkeys.json')
config_json = json.load(keyfile)
client_key = config_json["client_key"]
client_secret = config_json["client_secret"]
auth = requests.auth.HTTPBasicAuth(client_key, client_secret)
user_agent = config_json["user_agent"]
user_name = config_json["user_name"]
password = config_json["password"]

reddit = praw.Reddit(
    client_id=client_key,
    client_secret=client_secret,
    user_agent=user_agent,
    password=password,
    username=user_name
)


def get_pushshift_data(after, before, sub):
    result = []
    start = after
    while True:
        url = 'https://api.pushshift.io/reddit/search/submission/?sort = desc'+'&limit=1000&after='+str(start)+'&before='+str(before)+'&subreddit='+str(sub)
        r = requests.get(url)
        initial_data = json.loads(r.text)
        init_len = len(result)
        result += initial_data['data']
        updated_len = len(result)
        if updated_len == init_len or updated_len >= 10000:
            break
        start = (result[len(result) - 1])['created_utc']
        print(updated_len, "polled from api", end='', flush=True)
    return result


def sub_invalid(sub):
    invalid = False
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        invalid = True
    return invalid
