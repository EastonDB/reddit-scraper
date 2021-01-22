import praw  # reddit API Wrapper
import pandas as pd
import datetime as dt
import os

reddit_secret = os.environ.get('Reddit_Secret')
reddit_app_id = os.environ.get('Reddit_App_ID')
reddit_app_name = os.environ.get('Reddit_App_Name')
reddit_username = os.environ.get('Reddit_Username')
reddit_password = os.environ.get('Reddit_Password')
# verify and access reddit through api
reddit = praw.Reddit(client_id=reddit_app_id,
                     client_secret=reddit_secret,
                     user_agent=reddit_app_name,
                     username=reddit_username,
                     password=reddit_password)
# access Subreddit
subreddit = reddit.subreddit("food")
# search "title" for the string "chicken"
top_subreddit = subreddit.search("chicken", limit=None)
# create dictionary
topics_dict = {"author": [],
               "subreddit": [],
               "domain": [],
               "url": [],
               "title": [],
               "body": [],
               "score": [],
               "id": [],
               "comms_num": [],
               "created": []}
#  iterate through top_subreddit object and append the info to the dictionary
for submission in top_subreddit:
    topics_dict["author"].append(submission.author)
    topics_dict["subreddit"].append(submission.subreddit)
    topics_dict["domain"].append(submission.domain)
    topics_dict["url"].append(submission.url)
    topics_dict["title"].append(submission.title)
    topics_dict["body"].append(submission.selftext)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
# put data into a dataframe
topics_data = pd.DataFrame(topics_dict)


# function to clean up unix timestamps
def get_date(created):
    return dt.datetime.fromtimestamp(created)


_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp=_timestamp)
# export final file into a csv, with primary key removed
topics_data.to_csv('sample_reddit_file.csv', index=False)
