import tweepy

from csv_write import csv_write

def get_userInfo(author_id):
    consumer_key = "" #Your API/Consumer key 
    consumer_secret = "" #Your API/Consumer Secret Key
    access_token = ""    #Your Access token key
    access_token_secret = "" #Your Access token Secret key

    Bearer_Token = ""
    user_field = ["created_at","description","entities","id","location","name","pinned_tweet_id","profile_image_url","protected","url","username","verified","withheld"]


    data = tweepy.Client(Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict).get_user(id=author_id,user_fields=user_field)
    # print(data)
    for x in data:
        user_data=[]
        for title in data[x]:
            item=data[x]
            if(title=="id"):
                user_data.insert(0,item[title])
            if(title=="name"):
                user_data.insert(1,item[title])
            if(title=="username"):
                user_data.insert(2,item[title])
            if(title=="location"):
                user_data.insert(3,item[title])
            if(title=="profile_image_url"):
                user_data.insert(4,item[title])
            if(title=="created_at"):
                user_data.insert(5,item[title])
            if(len(user_data)==6):
                csv_write("user_data.csv",user_data)
        # data = tweepy.Client(Bearer_Token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict).get_users_followers(id=author_id)
        