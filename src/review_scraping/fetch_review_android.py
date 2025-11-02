import time
import pandas as pd
from google_play_scraper import reviews, reviews_all

app_list = pd.read_csv("../app-list.csv")

for i in range(len(app_list)):
    continuation_token = None
    app_reviews = []
    cnt = 0

    if app_list.iloc[i]["Category"] != "Object & Text Recognition":
        continue

    while True:
        result = reviews(
            app_list.iloc[i]["GoogleID"],
            lang='en',  # defaults to 'en'
            country='gb',  # defaults to 'us'
            continuation_token=continuation_token
        )

        cnt += 1

        continuation_token = result[1]
        if len(result[0]) == 0:
            break

        for res in result[0]:
            app_reviews.append({
                "rating": res["score"],
                "review": res["content"],
                "like count": res["thumbsUpCount"],
                "date": res["at"].strftime("%Y-%m-%d %H:%M:%S")
            })

        time.sleep(30)
    
    app_name = app_list.iloc[i]["Name"]
    print(f"total reviews fetched for {app_name}: {len(app_reviews)}")
    pd.DataFrame(app_reviews).to_csv(f"../dataset/android/{app_name}.csv", index=False, sep=",")

