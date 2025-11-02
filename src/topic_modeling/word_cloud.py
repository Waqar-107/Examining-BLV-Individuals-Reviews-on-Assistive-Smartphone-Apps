import spacy
import pandas as pd
from wordcloud import WordCloud

# Load spaCy model once
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def preprocess(texts):
    processed_texts = []

    try:
        for doc in nlp.pipe(texts, batch_size=50):
            tokens = [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop and not token.is_punct and token.is_alpha
            ]
            processed_texts.append(" ".join(tokens))
    except Exception as e:
        print(e)
        print(doc)
        exit(1)
        
    return processed_texts

def generate_wordcloud(csv_path, text_column, output_path):
    df = pd.read_csv(csv_path)
    
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in {csv_path}")
    
    df["processed"] = preprocess(df[text_column])
    long_string = ' '.join(df["processed"])

    wordcloud = WordCloud(
        background_color="white",
        max_words=1000,
        contour_width=3,
        contour_color='steelblue'
    ).generate(long_string)

    wordcloud.to_file(output_path)
    print(f"Word cloud saved to: {output_path}")


generate_wordcloud("../dataset/navigation_reviews.csv", "review", "../dataset/navigation_wordcloud.png")
generate_wordcloud("../dataset/object_and_text_recognition_reviews.csv", "review", "../dataset/ocr_wordcloud.png")