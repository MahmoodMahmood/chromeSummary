# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 04:27:29 2018

@author: Paul
"""

from nltk import tokenize as tk;
from nltk import corpus;
from nltk import stem;
import pandas as panda
import tensorflow as tf
import numpy as np
import math as math
import json 
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions

def stemmedPunctuationTokenized(sentence):
    s = stem.PorterStemmer()
    tokenizer = tk.RegexpTokenizer(r'\w+')
    words = [s.stem(w) for w in tokenizer.tokenize(sentence) if not w in stopword]
    return " ".join(words) 

urlTarget='https://www.sciencedirect.com/science/article/pii/037838129502717S'
nRelevance=10
compressionRate=0.70 
nSent = 4
sess = tf.Session()
nl = NaturalLanguageUnderstandingV1(
  username='8715593f-3e96-4ea1-9f00-e1c3acd86c3f',
  password='aTtMyOouU4Is',
  version='2017-02-27')

response = nl.analyze(
  url=urlTarget,
  features=Features(
    #entities=EntitiesOptions(emotion=True,sentiment=True,limit=2),
    keywords=KeywordsOptions(limit=nRelevance+1)),
  return_analyzed_text=True)
  
  
  
stopword = set(corpus.stopwords.words("english"));
article = tk.sent_tokenize(response["analyzed_text"])

keywords = response['keywords']
print(keywords)
sentRelevance = []
s = stem.PorterStemmer();
for sent in article:
    
    #Punctuation Filtered as well
    #tokenizer = tk.RegexpTokenizer(r'\w+')
    #words = [s.stem(w) for w in tokenizer.tokenize(sent) if not w in stopword]
    #Below keeps punctuation
    #words = [s.stem(w) for w in tk.word_tokenize(sent) if not w in stopword]
   # print(words)
    #stemmedSent = " ".join(words)    
    #print(stemmedSent)
    score = [k['relevance'] for k in keywords if stemmedPunctuationTokenized(sent).lower().find(stemmedPunctuationTokenized(k['text']).lower())!=-1]
    print(score)
    floatscore = [float(number) for number in score ]
    sentRelevance.append(np.sum(floatscore))
    
totalSent = np.size(sentRelevance)
#nSentActual = math.floor(totalSent*(1-compressionRate))
nSentActual = min(nSent,totalSent)
relevantV,indicies =tf.nn.top_k(tf.constant(sentRelevance),k=nSentActual)
indexZeros = tf.reshape(tf.where(tf.equal(relevantV,0)),[-1])
indexAll = tf.expand_dims(tf.range(0,tf.shape(indicies)[0]),0)
flatIndexAll = tf.reduce_sum(indexAll,0)

print(sess.run(relevantV))
print(sess.run(indicies))
print(sess.run(indexZeros))
print(sess.run(flatIndexAll))

validSet= tf.setdiff1d(flatIndexAll,tf.cast(indexZeros,dtype=tf.int32))
indexNonZero = sess.run(tf.gather(indicies,validSet[0]))

print(sess.run(validSet[0]))
print((indexNonZero))

relevantSentences = np.take(article,np.sort(indexNonZero))
joinedRelevance = " ".join(relevantSentences)
print("Summary Size %d:"%(len(indexNonZero)))
print(joinedRelevance)
#print(sess.run(tf.shape(tf.concat(relevantSentences,0))))
print("Original:")
print(" ".join(article))
#for sent in article:
 #   for w in stopword:
  #      if 
#print ((article))
print((sentRelevance))
#print(article)