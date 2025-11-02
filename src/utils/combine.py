import os
import pandas as pd

files = os.listdir("../dataset/android")
res = []

for file in files:
  try:
    df = pd.read_csv("../dataset/android/" + file)
    app_name = file.split(".")[0]

    for i in range(len(df)): 
      res.append({
        "app name": app_name,
        "rating": df.iloc[i]["rating"],
        "review": df.iloc[i]["review"],
        "like count": df.iloc[i]["like count"],
        "date": df.iloc[i]["date"],
      })
  except Exception as e:
    print(e)

print("total reviews fetched for Object & Text Recognition: ", len(res))
pd.DataFrame(res).to_csv("../dataset/android_reviews_object_and_text_recognition.csv", index=False, sep=",")