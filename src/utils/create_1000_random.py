import pandas as pd

df = pd.read_csv("../dataset/all_reviews_randomized_master.csv")

# save the blinds in a separate file
df_non_blind = df[df['bvi_keywords_auto'].notna() == False]
print("non-blind reviews:", len(df_non_blind))

# Filter rows where 'review' has at least 5 words
filtered_df = df_non_blind[df_non_blind['review'].str.split().str.len() >= 5]
print("Filtered reviews with at least 5 words:", len(filtered_df))

# Take 1000 random samples
sampled_df = filtered_df.sample(n=1000, random_state=42)
print("Sampled reviews:", len(sampled_df))

sampled_df.to_csv("../dataset/for_manual/random_1000_master.csv")