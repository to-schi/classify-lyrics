from farben import color
import my_stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from imblearn.under_sampling import RandomUnderSampler
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.pipeline import make_pipeline
import os
import argparse

parser = argparse.ArgumentParser(
    description="This program will show the probability of certain lyrics being from one of the artists in the dataframe")
parser.add_argument(
    "text_file", help="lyrics to guess as text-file", type=str, nargs='?', default="test_song.txt")
parser.add_argument(
    "dataframe", help="dataframe to prozess as csv-file", nargs='?')
args = parser.parse_args()
text_file = args.text_file
dataframe = args.dataframe
if dataframe == None:
    dataframe = "./lyrics_dataframe.csv"
if os.path.isfile(text_file):
    f = open(text_file, "r", encoding="utf-8")
    lyrics = f.read()
    f.close()
else: lyrics = text_file
df = pd.read_csv(dataframe)
labels = df['labels']
corpus = df.drop(columns='labels')
rus = RandomUnderSampler(sampling_strategy="auto", random_state=10)
corpus, labels = rus.fit_resample(corpus, labels)
corpus = corpus["songs"]

def clean_text(song):
    lemmatizer = WordNetLemmatizer()
    stop_words = my_stopwords.english #stopwords.words('english')
    words = word_tokenize(str(song).lower())
    filtered_words = []
    for word in words:
        if word not in stop_words and word.isalpha():
            word = lemmatizer.lemmatize(word, pos="v")
            filtered_words.append(word)
    return " ".join(filtered_words)

def clean_corpus(corpus):
    clean_corpus = []
    for song in corpus:
        cleaned_song = clean_text(song)
        clean_corpus.append(cleaned_song)
    return clean_corpus

def train_model(X_train, y_train):
    pipeline = make_pipeline(TfidfVectorizer(max_features=3000, min_df=2, max_df=0.8, ngram_range=(
        1, 1)), MultinomialNB(alpha=0.1))
    pipeline.fit(X_train, y_train)
    return pipeline

def classify(lyrics):
    pipeline = train_model(clean_corpus(corpus), labels)
    prediction = pipeline.predict([clean_text(lyrics)])
    probability = pipeline.predict_proba([clean_text(lyrics)])

    if probability.max().round(2) < 0.50:
        print("The artist is hard to guess! Maybe:"+color.yellow, prediction, color.end+" with a probability of:", color.green, probability.max().round(2), color.end)
        print(color.cyan, pd.DataFrame(probability, columns=pipeline.classes_), color.end)
        print(clean_text(lyrics))
    else:
        print("The artist is:"+color.yellow, prediction, color.end, "with a probability of: ", color.green, probability.max().round(2), color.end)
        print(color.cyan, pd.DataFrame(probability, columns=pipeline.classes_), color.end)
        print(clean_text(lyrics))

classify(lyrics)









