import pandas as pd
import spacy
from gensim import corpora
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser

# Load spaCy model for lemmatization and tokenization
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

custom_stopwords = set([
    "app", "good", "great", "application", "use", "using", 
    "love", "like", "thank", "thanks", "work", "works"
])

def preprocess(texts):
    processed_texts = []

    try:
        for doc in nlp.pipe(texts, batch_size=50):
            tokens = [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop and not token.is_punct and token.is_alpha and token.lemma_.lower() not in custom_stopwords
            ]
            processed_texts.append(tokens)
    except Exception as e:
        print(e)
        print(doc)

        exit(1)
    return processed_texts


def determine_LDA(texts, num_topics, print_topics=False):
    # Dictionary: maps words to IDs
    dictionary = corpora.Dictionary(texts)

    # Corpus: List of bag-of-words vectors
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,  # You can tune this
        passes=10,     # Number of training passes
        random_state=42
    )

    # view topics
    if print_topics:
        for i, topic in lda_model.show_topics(formatted=True):
            print(f"Topic #{i}: {topic}")

    # assign topics
    topics = []
    for i, bow in enumerate(corpus):
        topic_scores = lda_model.get_document_topics(bow)
        dominant_topic = max(topic_scores, key=lambda x: x[1])
        topics.append(dominant_topic[0])

    coherence_model = CoherenceModel(
        model=lda_model, 
        texts=texts, 
        dictionary=dictionary, 
        coherence='c_v'
    )

    print('Perplexity: ', lda_model.log_perplexity(corpus))  
    print('Coherence Score: ', coherence_model.get_coherence())
    print()

    return topics


# Function to apply bigrams
def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]


# Read data
df = pd.read_csv("navigation_reviews.csv")

df.dropna()
processed_texts = preprocess(df["review"].tolist())
# df["processed_review"] = processed_texts

# Train bigram model
bigram = Phrases(processed_texts, min_count=5, threshold=100)
bigram_mod = Phraser(bigram)

# Apply bigrams to your processed texts
texts_bigrams = make_bigrams(processed_texts)

for i in range(5, 21):
    topics = determine_LDA(texts_bigrams, i, print_topics=True)