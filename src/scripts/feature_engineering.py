import os, sys
import pandas as pd
import en_core_web_sm
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.matcher import Matcher


def tf_idf(corpus, n=100, ngram=(1)):
    vectorizer = TfidfVectorizer(max_features=n, ngram_range=ngram)
    vectors = vectorizer.fit_transform(corpus)
    names = vectorizer.get_feature_names()
    data = vectors.todense().tolist()
    return names, data

def custom_matcher(nlp, doc_col, pattern=[], pattern_name=''):
    # initialize matcher
    matcher = Matcher(nlp.vocab)

    # specify match pattern
    matcher.add(pattern_name, pattern)

    res_df = pd.DataFrame(columns = [pattern_name, pattern_name+'_count'])
    # create two columns with counts/ presence of the match respectively
    for i, doc in doc_col.iteritems():
        match = matcher(doc)
        count = len(match)
        res_df.loc[i, pattern_name+'_count'] = count
        res_df.loc[i, pattern_name] = True if count>0 else False
    return res_df
