## Libraries
import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import en_core_web_sm
from collections import Counter
from spacy.matcher import PhraseMatcher, Matcher
import sys, os

# to import Database class from data_collection folder
module_path = os.path.abspath('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection')
if module_path not in sys.path:
    sys.path.append(module_path)

# now that the folder is in the path, ../data_collection/database.py can be imported
from database import Database

### setup logging file ###
# log into a text file
sys.stdout = open( '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/features/feature_engineering/Feature_Engineering_v5_log.txt', "w")

###################################################################################################

## import review, restaurant, and target data

db = Database()
# get halal-reviews (reviews that include the word 'halal')
reviews_sql = '''SELECT * FROM reviews'''
reviews_df = db.select_df(reviews_sql)
print('- {} reviews containing the word halal were scraped'.format(reviews_df.shape[0]))

# get target restaurants-of-interest list
file_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/features/target_feature/label_target.csv'
target_df = pd.read_csv(file_path, index_col=0)
target_df['halal'] = target_df['halal'].str.replace('FLASE', 'FALSE')
target_df['halal'] = target_df['halal'].apply(lambda x: True if x =='TRUE' else False)
halal_frac = target_df['halal'].sum()/target_df.shape[0]

print('- {:.0f}% of the {} restaurants-of-interest are halal'.format(halal_frac*100, target_df.shape[0]))

# patch missing platform_ids and mismatch in target data

# import original businesses data
rest_sql = '''SELECT * FROM businesses WHERE url LIKE '%yelp%' '''
rest_df = db.select_df(rest_sql)

# drop Aya Kitchen
aya_id = 'y6BfLt9Gvrq2JsJvjkjdIQ'
reviews_df.drop(reviews_df[reviews_df['restaurant_id'] == aya_id].index, inplace=True)

# patch platform_id in target_df
target_df = target_df.merge(rest_df[['platform_id', 'url']], how='left', on='url')
target_df.drop('platform_id_x', inplace=True, axis=1)
target_df = target_df.rename(columns={'platform_id_y' : 'platform_id'})
###################################################################################################

## Feature Engineering

# group reviews per restaurant
grouped_reviews_df = reviews_df.groupby('restaurant_id').agg(lambda x: ' '.join(x)) # combine review text
grouped_reviews_df['review_date'] = grouped_reviews_df['review_date'].apply(lambda x: x.split()) # make dates list
grouped_reviews_df['review_count'] = grouped_reviews_df['review_date'].apply(lambda x: len(x)) # count reviews per restaurnat
grouped_reviews_df.head()

# merge restaurant name to review data
grouped_reviews_df = grouped_reviews_df.merge(target_df[['platform_id', 'name', 'total_review_count', 'halal']], how='left', left_index=True, right_on='platform_id')

grouped_reviews_df.index = grouped_reviews_df['platform_id']
grouped_reviews_df.drop('platform_id', inplace=True, axis=1)
grouped_reviews_df = grouped_reviews_df.rename(columns={'name': 'restaurant_name', 'review_count' : 'halal_review_count'})

# 1. add categorical column for 'halal' in rest_name
grouped_reviews_df['halal_in_name'] = grouped_reviews_df.apply(lambda row: True if 'halal' in row['restaurant_name'].lower() else False, axis=1)

# 2. calculate percentage of halal-containing reviews out of total reviews
grouped_reviews_df['halal_review_percent'] = grouped_reviews_df.apply(lambda row: row['halal_review_count']/row['total_review_count'], axis =1)

# 3. run nlp of grouped review text and save Doc to dataframe
nlp = en_core_web_sm.load()
grouped_reviews_df['doc'] = grouped_reviews_df['review_text'].apply(lambda x: nlp(x))

def common_at_position_from_halal(doc_col, position=1, n=10):
    # initialize matcher
    matcher = Matcher(nlp.vocab)
    # specify match pattern
    pattern = [{'LOWER': 'halal'}]
    matcher.add('halal', None, pattern)
    word_freqs = Counter()
    # noun_freqs = Counter()
    for doc in doc_col:
        matches = matcher(doc)
        words = []
        nouns = []
        for match_id, start, end in matches:
            if start+position < len(doc):
                token = doc[start+position]
            else:
                break
            # all tokens that arent stop words, spaces or punctuations
            words.append(token.lemma_ if token.is_stop != True and token.is_punct != True and token.is_space != True else _)
            # # noun tokens that arent stop words or punctuations
            # nouns.append(token.lemma_ if token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN" else nouns
            # most common tokens
        word_freq = Counter(words)
        word_freqs = word_freqs + word_freq
        # # most common noun tokens
        # noun_freq = Counter(nouns)
        # noun_freqs = noun_freqs + noun_freq

    # common_nouns = noun_freqs.most_common(n)
    common_words = word_freqs.most_common(n)
    return common_words #, common_nouns

common_after_halal = common_at_position_from_halal(data_df['doc'], position=1, n=100)

# use words with more than 10 instances
more_than_10counts = [count[1] > 10 for count in common_after_halal]
words = np.array(common_after_halal)[more_than_10counts].tolist()
words = [word[0] for word in words]
words = words + [''] # to get total count of 'halal' in next function

def count_matches(doc_col, words):
    '''
    Input:
        - Pandas Series with Spacy Doc object for every restaurants' collection of reviews
    Output:
        - Pandas Dataframe with columns of counts of 'halal X' for X in arg:words. The counts are
          per restaurant reviews
    '''
    # dataframe with created columns
    df = pd.DataFrame(columns=['halal_' + word + '_count' for word in words], index=doc_col.index)
    # for progress reporting
    c=1
    for word in words:
        # initialize matcher
        matcher = Matcher(nlp.vocab)
        # specify match pattern
        if word:
            pattern = [{'LOWER': 'halal'}, {'LOWER': word}]
        else: # to account for empty string which is used to count 'halal' mentions per restaurant for normalization
            pattern = [{'LOWER' : 'halal'}]
        matcher.add('halal', None, pattern)
        for i, doc in doc_col.iteritems():
            matches = matcher(doc)
            col_name = 'halal_' + word + '_count'
            df.loc[i, col_name] = len(matches)
        print('[{}/{}]'.format(c, len(words)), end='\r', flush=True)
        c += 1
    return df

# get dataframe with counts of 'halal X' for X in list of words
new_features_df = count_matches(data_df['doc'], words)
# normalize by dividing by number of mentions by total 'halal' mentions per restaurant
new_features_df = new_features_df.apply(lambda col: col/grouped_reviews_df['halal__count'])
# change column names from _count to _frequency
change_names = dict((old_name, old_name.replace('count', 'freq')) for old_name in df.columns[:-1])
new_features_df.rename(columns=change_names, inplace=True)
