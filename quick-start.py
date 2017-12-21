#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 22:53:32 2017

@author: qin
"""
import tempfile
import os.path
import logging
from gensim import corpora
from gensim import models
K=2; #number of topics


raw_corpus = []
with open("tweet_text.csv") as file:
   for line in file:
       raw_corpus.append(line) 
file.close()
# no = len(raw_corpus)

# raw_corpus = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",              
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]

# Create a set of frequent words
stoplistf= open("stopwords.txt")
stoplist=stoplistf.read()
stoplist.split('\n')

#stoplist = set('for a of the and to in'.split(' ')) # we have a stopword list
# Lowercase each document, split it by white space and filter out stopwords
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in raw_corpus]

# Count word frequencies
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]


dictionary = corpora.Dictionary(processed_corpus)

#new_doc = "Human computer interaction"
#new_vec = dictionary.doc2bow(new_doc.lower().split())
#new_vec

bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
#bow_corpus


# train the model
tfidf = models.TfidfModel(bow_corpus) # step 1 -- initialize a model
# transform the "system minors" string
#tfidf[dictionary.doc2bow("system minors".lower().split())]



#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



#TEMP_FOLDER = tempfile.gettempdir()
#print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))

#tfidf = models.TfidfModel(corpus) 

#doc_bow = [(0, 1), (1, 1)]
#print(tfidf[doc_bow]) # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[bow_corpus]
for doc in corpus_tfidf:
    print(doc)
    
#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
#corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

lda_tfidf = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=K)    
corpus_lda_tfidf=lda_tfidf[corpus_tfidf]




for doc in corpus_lda_tfidf:
    print(doc)

#print(dictionary)

print(dictionary.token2id)

#print topics 
lda_tfidf.print_topics(K)


