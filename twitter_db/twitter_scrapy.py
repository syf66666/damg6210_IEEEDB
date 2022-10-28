from http import client
from operator import le
from sre_parse import expand_template
from attr import field
import tweepy

from csv_write import csv_write
from user_info import get_userInfo
consumer_key = "WXFZl0njFIHtkGe4WtaKJ86zA" #Your API/Consumer key 
consumer_secret = "gspUqVootUgXIsT054x8CkYte6KbtUpRatz9PaxWYzTc2aWckh" #Your API/Consumer Secret Key
access_token = "1582856167797276673-ief9RoNBDiTTlty6srFOgXlteNY9vA"    #Your Access token key
access_token_secret = "1sK5h3ab7oLjZ2nyXNnEoHx124BeAT1LhISGidJGU3hJc" #Your Access token Secret key

Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAJlziQEAAAAAMTzJICra4ARrD74ioqrGzhagivQ%3DFQdBuxlHQgDzyFmRPc9zhA6X6pyLXhq4PNCkR1D4MaRIP96D25"


tweet_field=["attachments","author_id","context_annotations","created_at","entities","geo","id","in_reply_to_user_id","lang","possibly_sensitive","public_metrics","referenced_tweets","source","text","withheld"]
user_field = ["created_at","description","entities","id","location","name","pinned_tweet_id","profile_image_url","protected","url","username","verified","withheld"]

tweets = tweepy.Client(
   Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict
).search_recent_tweets(query="computer",start_time="2022-10-21T23:00:00Z",end_time="2022-10-27T18:00:00Z",max_results=100,tweet_fields=["attachments","author_id","context_annotations","created_at","entities","geo","id","in_reply_to_user_id","lang","possibly_sensitive","public_metrics","referenced_tweets","source","text","withheld"])

for x in tweets:
    for item in tweets[x]:
        tweet_data=[]
        public_metrics=[]
        referenced_tweets=[]
        if(type(item)!=str):
            for title in item:
                if(title=="id"):
                    tweet_data.insert(0,item[title])
                    public_metrics.insert(0,item[title])
                    referenced_tweets.insert(0,item[title])
                if(title=="public_metrics"):
                    for key in item[title]:
                        public_metrics.append(item[title][key])
                if(title=="author_id"):
                    tweet_data.insert(1,item[title])
                if(title=="text"):
                    tweet_data.insert(2,item[title])
                if(title=="created_at"):
                    tweet_data.insert(3,item[title])
                if(title=="source"):
                    tweet_data.insert(4,item[title])
                if(title=="referenced_tweets"):
                    for i in item[title]:
                        for key in i:
                            referenced_tweets.append(i[key])
                if(title=="author_id"):
                    author_id = item[title]
                    get_userInfo(author_id)
                if(len(tweet_data)==5):
                    print(tweet_data)
                    csv_write("tweets.csv",tweet_data)
                if(len(public_metrics)==5):
                    print(public_metrics)
                    csv_write("public_metrics.csv",public_metrics)
                if(len(referenced_tweets)==3):
                    print(referenced_tweets)
                    csv_write("referenced_tweets.csv",referenced_tweets)

# print(client)
# user_field = ["created_at","description","entities","id","location","name","pinned_tweet_id","profile_image_url","protected","url","username","verified","withheld"]
# user_data = tweepy.Client(
#    Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict
# ).search_recent_tweets(query="computer",start_time="2022-10-21T23:00:00Z",end_time="2022-10-27T18:00:00Z",max_results=100,user_fields=user_field)
# for x in user_data:
#     for item in user_data[x]:
#         print(item)