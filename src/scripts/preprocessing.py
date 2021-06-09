import os, sys
import pandas as pd
import en_core_web_sm
import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc
import numpy
import re
from spacy.matcher import Matcher

# to import Database class from data_collection folder
module_path = os.path.abspath(os.path.join('../..')+'/data/data_collection')
if module_path not in sys.path:
    sys.path.append(module_path)

# now that the folder is in the path, ../data_collection/database.py can be imported
from storage_managers.database import Database


def fetch_data() -> pd.DataFrame():
    db = Database()
    # get halal-reviews and its restaurant data
    data_sql = '''SELECT b.platform_id, b.name as restaurant_name, r.review_text, r.username, r.rating,
                concat(review_date,date) as review_date, r.helpful_count, b.address, b.image_url,
                b.lat, b.lng, b.total_review_count, b.total_halal_review_count
                FROM reviews r
                JOIN businesses b
                ON r.restaurant_id = b.platform_id
                WHERE r.review_text IS NOT NULL '''
    data_df = db.select_df(data_sql)
    return data_df

def format_columns(data_df) -> pd.DataFrame():
    str_to_num_cols = ['rating']
    for col in str_to_num_cols:
        data_df[col] = data_df[col].str.extract('(\d+)')
        data_df[col].fillna(-1, inplace=True)
        data_df[col] = data_df[col].astype(int)

    str_to_lower = ['restaurant_name', 'review_text', 'username']
    for col in str_to_lower:
        data_df[col] = data_df[col].str.lower()
    return data_df


def collapse_reviews(data_df, f = {}, agg_col = '') -> pd.DataFrame():
    # combine  reviews text per restaurant
    for col in data_df.columns[data_df.columns != agg_col_col]:
        if col not in f.keys():
            f[col] = 'first'
    collapsed_df = data_df.groupby(agg_col, as_index=False).agg(f)
    return collapsed_df
    ### ignore these for now:
    ## include date info? then have to consider classification per review and how to aggregate classifications
    #  per restaurant?


def clean_review_text(data_df, save_doc = True) -> pd.DataFrame():
    # initialize NLP tools
    punctuations = string.punctuation
    stop_words = STOP_WORDS
    nlp = en_core_web_sm.load()

    # column containing review texts
    reviews_col = data_df.columns[ data_df.columns.str.contains('text')][0]
    if save_doc:
        # initialize column to save Spacy doc object
        data_df['doc'] = ''

    for i, text in data_df[reviews_col].items():
        ## clean (convert to lowercase and remove punctuations and   characters and then strip)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
        ## Tokenize (convert from string to list)
        lst_text = text.split()
        ## remove Stopwords
        lst_text = [word for word in lst_text if word not in STOP_WORDS]
        ## save Spacy doc object
        doc = nlp(' '.join(lst_text)[:1000000])
        if save_doc:
            data_df.at[i, 'doc'] = doc
        ## Lemmatisation (convert the word into root word)
        lem_doc = [word.lemma_ for word in doc]
        ## back to string from list
        data_df.loc[i, 'clean_text'] = ' '.join(lem_doc)

    return data_df
