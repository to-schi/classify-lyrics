"""
Command line tool to show the probability of certain
lyrics being from one of the artists in the dataframe.
"""
# pylint: disable=line-too-long
import argparse
import os

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

import utils.my_stopwords
from utils.farben import Color

parser = argparse.ArgumentParser(
    description="This program will show the probability of certain lyrics being from one of the artists in the dataframe"
)
parser.add_argument(
    "text_file",
    help="lyrics to guess as text-file",
    type=str,
    nargs="?",
    default="test_song.txt",
)
parser.add_argument("dataframe", help="dataframe to prozess as csv-file", nargs="?")
args = parser.parse_args()
TEXT_FILE = args.text_file
DATAFRAME = args.dataframe
if DATAFRAME is None:
    DATAFRAME = "./lyrics_dataframe.csv"
if os.path.isfile(TEXT_FILE):
    f = open(TEXT_FILE, "r", encoding="utf-8")
    lyrics = f.read()
    f.close()
else:
    lyrics = TEXT_FILE
df = pd.read_csv(DATAFRAME)
labels = df["labels"]
corpus = df.drop(columns="labels")
rus = RandomUnderSampler(sampling_strategy="auto", random_state=10)
corpus, labels = rus.fit_resample(corpus, labels)  # type: ignore
corpus = corpus["songs"]


def clean_text(song):
    """
    Filters text for stop_words (list) and lemmatizes each remaining word.
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = utils.my_stopwords.english  # stopwords.words('english')
    words = word_tokenize(str(song).lower())
    filtered_words = []
    for word in words:
        if word not in stop_words and word.isalpha():
            word = lemmatizer.lemmatize(word, pos="v")
            filtered_words.append(word)
    return " ".join(filtered_words)


def clean_corpus(texts):
    """
    Iterates over the whole corpus and applies "clean_text" to every entry. 
    """
    cleaned_corpus = []
    for song in texts:
        cleaned_song = clean_text(song)
        cleaned_corpus.append(cleaned_song)
    return cleaned_corpus


def train_model(x_train, y_train):
    """creates model pipeline and returns trained model"""
    pipeline = make_pipeline(
        TfidfVectorizer(max_features=3000, min_df=2, max_df=0.8, ngram_range=(1, 1)),
        MultinomialNB(alpha=0.1),
    )
    pipeline.fit(x_train, y_train)
    return pipeline


def classify(text):
    """gets the probabilities from the model"""
    pipeline = train_model(clean_corpus(corpus), labels)
    prediction = pipeline.predict([clean_text(text)])
    probability = pipeline.predict_proba([clean_text(text)])

    if probability.max().round(2) < 0.50:
        print(
            "The artist is hard to guess! Maybe:" + Color.yellow,
            prediction,
            Color.end + " with a probability of:",
            Color.green,
            probability.max().round(2),
            Color.end,
        )
        print(
            Color.cyan, pd.DataFrame(probability, columns=pipeline.classes_), Color.end
        )
        print(clean_text(text))
    else:
        print(
            "The artist is:" + Color.yellow,
            prediction,
            Color.end,
            "with a probability of: ",
            Color.green,
            probability.max().round(2),
            Color.end,
        )
        print(
            Color.cyan, pd.DataFrame(probability, columns=pipeline.classes_), Color.end
        )
        print(clean_text(text))


classify(lyrics)
