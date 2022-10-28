import csv

from pip import main
def csv_write(file_name,data_toappend):
    data = data_toappend
    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# csv_write("user_data.csv",["user_id","name","username","location","profile_image_url","created_at"])