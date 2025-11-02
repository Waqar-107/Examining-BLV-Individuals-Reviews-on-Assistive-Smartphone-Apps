import pandas as pd
import re
from datetime import datetime

def normalize(text):
    return re.sub(r'\s+', ' ', str(text).strip().lower())  # lowercase, strip, collapse all whitespace

files = [
  "../dataset/combined/navigation/android_reviews_navigation.csv",
  "../dataset/combined/navigation/ios_reviews_navigation.csv",
  "../dataset/combined/object_and_text_recognition/android_reviews_object_and_text_recognition.csv",
  "../dataset/combined/object_and_text_recognition/ios_reviews_object_and_text_recognition.csv"       
]

rating_mapper = {}
total = 0
dbg_key = ""

for file in files:
  df = pd.read_csv(file)
  total += len(df)

  for i in range(len(df)):
    review = normalize(df.iloc[i]["review"])
    app_name = df.iloc[i]["app name"].split(".")[0]

    try :
      key = review + "_" + app_name # + "_" + date
      
      rating_mapper[key] = int(df.iloc[i]["rating"])
    except Exception as e:
      print(e)
      print(review)
      print(app_name)

print("total reviews:", total)
print("in map:", len(rating_mapper.keys()))


df = pd.read_csv("../dataset/all_reviews_randomized_master.csv")
ratings = []
total_assigned = 0

for i in range(len(df)):
  review = normalize(df.iloc[i]["review"])
  app_name = df.iloc[i]["app_name"]

  try:
    key = review + "_" + app_name
    if key in rating_mapper.keys():
      ratings.append(rating_mapper[key])
      total_assigned += 1
    else:
      print("not in map")
      exit(0)
      ratings.append(0)
  except Exception as e:
    ratings.append(0)
    print(e)
    print(review)
    print(app_name)

    exit(0)

print("total assigned:", total_assigned, "out of", len(df))
df["rating"] = ratings
df.to_csv("../dataset/all_reviews_randomized_master_ratings.csv", index=False)
