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
  
def stemmedPunctuationTokenized(sentence,stopword=set(corpus.stopwords.words("english"))):
    s = stem.PorterStemmer()
    tokenizer = tk.RegexpTokenizer(r'\w+')
    words = [s.stem(w) for w in tokenizer.tokenize(sentence) if not w in stopword]
    return " ".join(words)

def wrapperSummary(url,nSent=4,nRelevance=10):
    urlTarget = url
    sess = tf.Session()
    nl = NaturalLanguageUnderstandingV1(
      username='8715593f-3e96-4ea1-9f00-e1c3acd86c3f',
      password='aTtMyOouU4Is',
      version='2017-02-27')
    #print(nRelevance)
    response = nl.analyze(
      url=urlTarget,
      #text="Different categories of gender very in the context they are in.",
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
        score = [k['relevance'] for k in keywords if stemmedPunctuationTokenized(sent,stopword).lower().find(stemmedPunctuationTokenized(k['text'],stopword).lower())!=-1]
        #print(score)
        floatscore = [float(number) for number in score ]
        sentRelevance.append(np.sum(floatscore))
    totalSent = np.size(sentRelevance)
    #nSentActual = math.floor(totalSent*(1-compressionRate))
    nSentActual = min(nSent,totalSent)
    relevantV,indicies =tf.nn.top_k(tf.constant(sentRelevance),k=nSentActual)
    indexZeros = tf.reshape(tf.where(tf.equal(relevantV,0)),[-1])
    indexAll = tf.expand_dims(tf.range(0,tf.shape(indicies)[0]),0)
    flatIndexAll = tf.reduce_sum(indexAll,0)
    
    validSet= tf.setdiff1d(flatIndexAll,tf.cast(indexZeros,dtype=tf.int32))
    indexNonZero = sess.run(tf.gather(indicies,validSet[0]))

    relevantSentences = np.take(article,np.sort(indexNonZero))
    joinedRelevance = " ".join(relevantSentences)
    return joinedRelevance


print(wrapperSummary("https://en.wikipedia.org/wiki/The_Tortoise_and_the_Hare"))


















'''
#BELOW IS THE CODE BEHIND THE SUMMARIZE FUNCTION WITH ALL ERROR CHECKING PRINTS
####################################################
urlTarget='https://www.google.ca/search?biw=1536&bih=686&ei=vLF2WoSzHIGwsAXWkY2ADA&q=tortoise+and+the+hare&oq=tortise+and+the+++&gs_l=psy-ab.3.0.0i10k1l10.16710.20655.0.21502.18.16.0.0.0.0.480.2051.7j7j4-1.15.0....0...1c.1.64.psy-ab..3.15.2036...0j0i67k1j0i131k1j0i46i67k1j46i67k1j0i131i67k1j0i10i46k1j46i10k1.0.QQnLXRCixV0'
nRelevance=15
compressionRate=0.70
nSent = 4
sess = tf.Session()
#with open('AAA.txt', 'r+',encoding="utf8") as myfile:
#   data=myfile.read()
#print(data)
nl = NaturalLanguageUnderstandingV1(
  username='8715593f-3e96-4ea1-9f00-e1c3acd86c3f',
  password='aTtMyOouU4Is',
  version='2017-02-27')

response = nl.analyze(
  url=urlTarget,
  #text="Different categories of gender very in the context they are in. Some tension between gender categories emerges from trying to define identities through the opposition of each other, which grounds the two in relation. Defining the power of each group and the value that their associated work provides, or which or if work is associated becomes a problem in this opposition. Beauvoir speaks to the concept of othering in her book “The Second Sex,” describing a way that the category women are defined solely in terms of their being different from men in her Western society. In this description, the category of man is taken to be the default while the category of women is taken to be a feature that distinguishes women from the default state as an ‘other.’ This definition by exclusion is a technique that can support meaning as blind inclusion voids it by blending categories and thus rendering them unintelligible, however this conception of default and other sets the societal pre-eminence as well standard of experience and value on men. Othering is a compelling way of easily defining categories, but it brings conflict through skewing power dynamics. Another facet of othering is in how it has an effect in intersectionality in also applying to other aspects of identity including race and sexuality. These different aspects complicate consideration of gender because there is no general experience of gender at the crux of all of these irremovable contextually-related aspects of identity that make people subjects of differing treatments.",
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
    #print(words)
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

'''