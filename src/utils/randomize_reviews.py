import pandas as pd

df = pd.read_csv("../dataset/all_reviews.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(df["app_name"].value_counts())
df.to_csv("../dataset/all_reviews_randomized.csv", index=False)