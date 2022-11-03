from http import client
from operator import le
from sre_parse import expand_template
from attr import field
import tweepy

from csv_write import csv_write
from user_info import get_userInfo
consumer_key = "9HYB8Tv9ljZvseR6WnX3dUEJw" #Your API/Consumer key
consumer_secret = "kfzBKpTbPQroRsfQPqDEeIpUPETjoDTy4yQjkXIbsclOw5O91k" #Your API/Consumer Secret Key
access_token = "1512114371979141133-OconYOT7bAxSI372vh2YcQepwGtpLM"    #Your Access token key
access_token_secret = "MxpR8RI38IHM5HhjcjodbUeQnSnVsjTMMbb4HRHhBu4V4" #Your Access token Secret key

Bearer_Token = "AAAAAAAAAAAAAAAAAAAAANUiigEAAAAAqHiFBV6rEvBGaFzV4iS1P7z6tsA%3D9ZjhCmpuGUYWp2IhoGOXk9INisEgWb4eOikxg6Bz9EQnKkRDzx"

tweet_field=["attachments","author_id","context_annotations","created_at","entities","geo","id","in_reply_to_user_id","lang","possibly_sensitive","public_metrics","referenced_tweets","source","text","withheld"]
user_field = ["created_at","description","entities","id","location","name","pinned_tweet_id","profile_image_url","protected","url","username","verified","withheld"]
media_fields = ["public_metrics"]
tweets = tweepy.Client(
   Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict
).search_recent_tweets(query="computer conference",start_time="2022-10-28T23:00:00Z",end_time="2022-11-02T18:00:00Z",max_results=100,tweet_fields=["attachments","author_id","context_annotations","created_at","entities","geo","id","in_reply_to_user_id","lang","possibly_sensitive","public_metrics","referenced_tweets","source","text","withheld"])

author_ids=[]



csv_write("hashtag.csv",["tweet_id","start","end","tag"],'w')
csv_write("tweets.csv",["tweet_id","author_id","text","created_at","source"],'w')
csv_write("public_metrics.csv",["tweet_id","retweet_count","reply_count","like_count","quote_count"],'w')
csv_write("referenced_tweets.csv",["tweet_id","type","ref_id"],'w')
csv_write("user_data.csv",["user_id","name","username","location","profile_image_url","created_at"],'w')

for x in tweets:
    for item in tweets[x]:
        tweet_data=['','','','','']
        public_metrics=[]
        referenced_tweets=[]
        if(type(item)!=str):
            for title in item:
                if(title=="id"):
                    tweet_data[0]=item[title]
                    public_metrics.insert(0,item[title])
                    referenced_tweets.insert(0,item[title])
                if(title=="public_metrics"):
                    for key in item[title]:
                        public_metrics.append(item[title][key])
                if(title=="author_id"):
                    tweet_data[1]=item[title]
                if(title=="text"):
                    tweet_data[2]=item[title]
                if(title=="created_at"):
                    tweet_data[3]=item[title]
                if(title=="source"):
                    tweet_data[4]=item[title]
                if(title=="referenced_tweets"):
                    for i in item[title]:
                        for key in i:
                            referenced_tweets.append(i[key])
                if(title=="entities"):
                    for a in item[title]:
                        if(a=="hashtags"):
                            for x in item[title][a]:
                                hashtag=[]
                                hashtag.append(item["id"])
                                for y in x:
                                    hashtag.append(x[y])
                                if('' not in hashtag):
                                    csv_write("hashtag.csv",hashtag)
                if(title=="author_id"):
                    author_ids.append(item[title])
                if('' not in tweet_data):
                    print(tweet_data)
                    csv_write("tweets.csv",tweet_data)
                if(len(public_metrics)==5):
                    print(public_metrics)
                    csv_write("public_metrics.csv",public_metrics)
                if(len(referenced_tweets)):
                    print(referenced_tweets)
                    csv_write("referenced_tweets.csv",referenced_tweets)
get_userInfo(author_ids)

# print(client)
# user_field = ["created_at","description","entities","id","location","name","pinned_tweet_id","profile_image_url","protected","url","username","verified","withheld"]
# user_data = tweepy.Client(
#    Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict
# ).search_recent_tweets(query="computer",start_time="2022-10-21T23:00:00Z",end_time="2022-10-27T18:00:00Z",max_results=100,user_fields=user_field)
# for x in user_data:
#     for item in user_data[x]:
#         print(item)
