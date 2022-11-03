import csv

from pip import main
def csv_write(file_name,data_toappend,a='a'):
    data = data_toappend
    with open(file_name, a) as file:
        writer = csv.writer(file)
        writer.writerow(data)

# csv_write("hashtag.csv",["tweet_id","start","end","tag"])