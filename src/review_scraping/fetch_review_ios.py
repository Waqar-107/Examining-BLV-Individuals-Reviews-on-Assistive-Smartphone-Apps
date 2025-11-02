import time
import pandas as pd
from app_store_web_scraper import AppStoreEntry


app_list = pd.read_csv("../app-list.csv")
all_reviews = []

for i in range(len(app_list)):
    if app_list.iloc[i]["Category"] != "Object & Text Recognition" or not pd.notna(app_list.iloc[i]["AppleID"]):
      continue

    try:
        # us
        app = AppStoreEntry(app_id=app_list.iloc[i]["AppleID"][2:], country="us")
        for review in app.reviews():
            all_reviews.append({
                "app name": app_list.iloc[i]["Name"],
                "rating": review.rating,
                "title": review.title,
                "review": review.content,
                "date": review.date.strftime("%Y-%m-%d %H:%M:%S")
            })

        # gb
        app = AppStoreEntry(app_id=app_list.iloc[i]["AppleID"][2:], country="gb")
        for review in app.reviews():
            all_reviews.append({
                "app name": app_list.iloc[i]["Name"],
                "rating": review.rating,
                "title": review.title,
                "review": review.content,
                "date": review.date.strftime("%Y-%m-%d %H:%M:%S")
            })

        print("fetched", len(all_reviews), "reviews from", app_list.iloc[i]["Name"],)
        # time.sleep(60)
    except Exception as e:
        print(e)

print("total reviews fetched for Object & Text Recognition: ", len(all_reviews))
pd.DataFrame(all_reviews).to_csv("../dataset/ios_reviews_object_and_text_recognition.csv", sep=",", index=False)