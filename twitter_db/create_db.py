import pymysql
import pandas as pd
import time
import datetime
#We will use connect() to connect to RDS Instance
#host is the endpoint of your RDS instance
#user is the username you have given while creating the RDS instance
#Password is Master pass word you have given 
db = pymysql.connect(host="localhost", user = "root", password="12345678", database="twitter")
# you have cursor instance here
cursor = db.cursor()
cursor.execute("select version()")
#now you will get the version of MYSQL you have selected on instance
data = cursor.fetchone()
# #Lets's create a DB
# sql = '''create database twitter'''
# cursor.execute(sql)
# cursor.connection.commit()
# #Create a table 
sql1 = "DROP TABLE IF EXISTS `tweets`;"
cursor.execute(sql1)
sql2 = '''
CREATE TABLE `tweets` (
  `tweet_id` varchar(32) NOT NULL,
  `author_id` varchar(255) DEFAULT NULL,
  `text` varchar(2555) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`)
);
'''
cursor.execute(sql2)


# tweet_id,retweet_count,reply_count,like_count,quote_count
sql3 = "DROP TABLE IF EXISTS `public_metrics`;"
cursor.execute(sql3)
sql4 = '''
CREATE TABLE `public_metrics` (
  `tweet_id` varchar(32) NOT NULL,
  `retweet_count` int DEFAULT 0,
  `reply_count` int DEFAULT 0,
  `like_count` int DEFAULT 0,
  `quote_count` int DEFAULT 0,
  PRIMARY KEY (`tweet_id`)
);
'''
cursor.execute(sql4)


#tweet_id,type,ref_id
sql5 = "DROP TABLE IF EXISTS `referenced_tweets`;"
cursor.execute(sql5)
sql6 = '''
CREATE TABLE `referenced_tweets` (
  `tweet_id` varchar(32) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `ref_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`)
);
'''
cursor.execute(sql6)

#user_id,name,username,location,profile_image_url,created_at
sql1 = "DROP TABLE IF EXISTS `user_info`;"
cursor.execute(sql1)
sql2 = '''
CREATE TABLE `user_info` (
  `user_id` varchar(32) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `profile_image_url` varchar(255) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);
'''
cursor.execute(sql2)


# tweet_id,start,end,tag
sql1 = "DROP TABLE IF EXISTS `hashtag`;"
cursor.execute(sql1)
sql2 = '''
CREATE TABLE `hashtag` (
  `tweet_id` varchar(32) NOT NULL,
  `start` varchar(255) DEFAULT NULL,
  `end` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL
);
'''
cursor.execute(sql2)

tweetData = pd.read_csv('./tweets.csv',index_col=False)
tweetData.head()
tweet_ids = set()
for i,row in tweetData.iterrows():
    sql = "INSERT INTO twitter.tweets VALUES (%s,%s,%s,%s,%s)"
    string = row[3]
    string = string.split(".")[0]
    element = datetime.datetime.strptime(string,"%Y-%m-%dT%H:%M:%S")
    t = element.timetuple()
    string = time.mktime(t)
    row[3] = str(string)
    if row[0] not in tweet_ids:
        cursor.execute(sql, tuple(row))
        tweet_ids.add(row[0])
        # print("Record inserted")
        # the connection is not autocommitted by default, so we 
        # must commit to save our changes
        cursor.connection.commit()

public_metrics_data = pd.read_csv('./public_metrics.csv',index_col=False)
public_metrics_data.head()
tweet_ids = set()
for i,row in public_metrics_data.iterrows():
    sql = "INSERT INTO twitter.public_metrics VALUES (%s,%s,%s,%s,%s)"
    if row[0] not in tweet_ids:
        cursor.execute(sql, tuple(row))
        tweet_ids.add(row[0])
        # print("Record inserted")
        # the connection is not autocommitted by default, so we 
        # must commit to save our changes
        cursor.connection.commit()


referenced_tweets = pd.read_csv('./referenced_tweets.csv',index_col=False)
referenced_tweets.head()
tweet_ids = set()
for i,row in referenced_tweets.iterrows():
    sql = "INSERT INTO twitter.referenced_tweets VALUES (%s,%s,%s)"
    if row[0] not in tweet_ids and str(row[1])!='nan':
        cursor.execute(sql, tuple(row))
        tweet_ids.add(row[0])
        # print("Record inserted")
        # the connection is not autocommitted by default, so we 
        # must commit to save our changes
        cursor.connection.commit()


user_info = pd.read_csv('./user_data.csv',index_col=False)
user_info.head()
user_ids = set()
for i,row in user_info.iterrows():
    sql = "INSERT INTO twitter.user_info VALUES (%s,%s,%s,%s,%s,%s)"
    if row[0] not in user_ids:
        cursor.execute(sql, tuple(row))
        user_ids.add(row[0])
        # print("Record inserted")
        # the connection is not autocommitted by default, so we 
        # must commit to save our changes
        cursor.connection.commit()


hashtag = pd.read_csv('./hashtag.csv',index_col=False)
hashtag.head()
for i,row in hashtag.iterrows():
    sql = "INSERT INTO twitter.hashtag VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    cursor.connection.commit()


# What user posted this tweet?
tweet_id = ("1587866593886978054",)
sql = "SELECT `author_id` FROM `tweets` WHERE `tweet_id`=%s"
cursor.execute(sql, tuple(tweet_id))
result = cursor.fetchone()

sql = "SELECT `username` FROM `user_info` WHERE `user_id`=%s"
cursor.execute(sql, tuple(result))
result = cursor.fetchone()

print("The user who posted this tweet is named: ", result)


# When did the user post this tweet?
tweet_id = ("1587866593886978054",)
sql = "SELECT `author_id` FROM `tweets` WHERE `tweet_id`=%s"
cursor.execute(sql, tuple(tweet_id))
result = cursor.fetchone()

sql = "SELECT `location` FROM `user_info` WHERE `user_id`=%s"
cursor.execute(sql, tuple(result))
result = cursor.fetchone()

print("The tweet location is: ", result)

# What tweets have this user posted in the past 24 hours?
tweet_id = ("1587866593886978054",)
sql = "SELECT `author_id`, `created_at` FROM `tweets` WHERE `tweet_id`=%s"
cursor.execute(sql, tuple(tweet_id))
result = cursor.fetchone()

sql = "SELECT `tweet_id` FROM `tweets` WHERE `author_id`=%s AND `created_at`>=%s AND `created_at`<=%s"
# 24 hours = 86400 seconds
params = [result[0], float(result[1])-86400, float(result[1]) ]
cursor.execute(sql, tuple(params))
result = cursor.fetchone()
print("The tweets this user posted for last 24 hours are: ", result)


# How many tweets have this user posted in the past 24 hours?

tweet_id = ("1587866593886978054",)
sql = "SELECT `author_id`, `created_at` FROM `tweets` WHERE `tweet_id`=%s"
cursor.execute(sql, tuple(tweet_id))
result = cursor.fetchone()

sql = "SELECT COUNT(*) FROM `tweets` WHERE `author_id`=%s AND `created_at`>=%s AND `created_at`<=%s"

# 24 hours = 86400 seconds
params = [result[0], float(result[1])-86400, float(result[1]) ]
cursor.execute(sql, tuple(params))
result = cursor.fetchone()
print("The tweets count this user posted for last 24 hours is: ",result[0])


# When did this user join Twitter?
user_id=["1022648566194483201"]
sql = "SELECT `created_at` FROM `user_info` WHERE `user_id`=%s"
cursor.execute(sql, tuple(user_id))
result = cursor.fetchone()
print("This user created his twitter account in: ", result[0])


# What keywords/ hashtags are popular?
sql ='''
SELECT
tag,
COUNT(tag) AS `value_occurrence` 

FROM
  hashtag

GROUP BY 
  tag
ORDER BY 
  `value_occurrence` DESC
'''
cursor.execute(sql)
result = cursor.fetchone()
print("The most popular hashtag is: ", result[0])


# What tweets are popular?
sql ='''
SELECT
tweet_id,
like_count
FROM
  public_metrics
GROUP BY 
  tweet_id
ORDER BY 
  `like_count` DESC
LIMIT 1;
'''
cursor.execute(sql)
result = cursor.fetchone()
print("The most popular tweet is: ", result[0])


#Use Cases

