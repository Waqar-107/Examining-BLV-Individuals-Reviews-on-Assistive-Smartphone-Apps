import pandas as pd
import re
from datetime import datetime

df = pd.read_csv("../dataset/all_reviews_12229_randomized_master.csv")
df['date'] = pd.to_datetime(df['date'])

min_date = df['date'].min()
max_date = df['date'].max()

print(f"Minimum date: {min_date}")
print(f"Maximum date: {max_date}")