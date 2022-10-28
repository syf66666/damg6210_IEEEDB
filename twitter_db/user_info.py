import tweepy

from csv_write import csv_write

def get_userInfo(author_id):
    consumer_key = "WXFZl0njFIHtkGe4WtaKJ86zA" #Your API/Consumer key 
    consumer_secret = "gspUqVootUgXIsT054x8CkYte6KbtUpRatz9PaxWYzTc2aWckh" #Your API/Consumer Secret Key
    access_token = "1582856167797276673-ief9RoNBDiTTlty6srFOgXlteNY9vA"    #Your Access token key
    access_token_secret = "1sK5h3ab7oLjZ2nyXNnEoHx124BeAT1LhISGidJGU3hJc" #Your Access token Secret key

    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAJlziQEAAAAAMTzJICra4ARrD74ioqrGzhagivQ%3DFQdBuxlHQgDzyFmRPc9zhA6X6pyLXhq4PNCkR1D4MaRIP96D25"
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
        