import pandas as pd
import re

blv_keywords = pd.read_csv("../blv_keywords_unique.csv")
df = pd.read_csv("../dataset/all_reviews_randomized_master.csv")
utilized = {}
total = 0
res = []

for i in range(len(df)):
  review = df.iloc[i]["review"].lower()

  arr = []
  for key in blv_keywords["Keywords"]:
    if re.search(rf'\b{re.escape(key.lower())}\b', review):
      if key.lower() not in utilized:
        utilized[key.lower()] = 1
      else:
        utilized[key.lower()] += 1

      arr.append(key.lower())

  res.append(";".join(arr))
  if len(arr) > 0:
    total += 1

print("total blind related:", total, "out of", len(df), "reviews")

df["blv_keywords"] = res
df.to_csv("../dataset/all_reviews_randomized_master_blv.csv", index=False)