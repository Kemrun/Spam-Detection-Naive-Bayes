# -*- coding: utf-8 -*-
"""Spam Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xFB-myFew8mnf7E9w5zr5oSOKK8FOZ-k

# Spam Detection Classifier Naive Bayes
"""

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score,ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB
from wordcloud import WordCloud

!wget https://lazyprogrammer.me/course_files/spam.csv

df = pd.read_csv('spam.csv', encoding='ISO-8859-1')

df.head()

df = df.drop(['Unnamed: 2','Unnamed: 3', 'Unnamed: 4'], axis=1)
df.head()

#axis =1 is column

#renaming
df.columns =['labels','data']
df.head()

df.labels.hist()
# see that we have imbalanced data. Ham > spam/ So we have to check F1 SCORE

#we have to rename all the ham & spam to 1 and 0
# must create a new column with 1 - 0

df['b_labels'] = df['labels'].map({'ham':0, 'spam':1})
Y= df['b_labels'].to_numpy()

df.head(4)

#have a data. we need to split data uje

df_train, df_test, Ytrain, Ytes = train_test_split(df['data'], Y)

featurizer = CountVectorizer(decode_error='ignore')

Xtrain = featurizer.fit_transform(df_train)
Xtest = featurizer.transform(df_test)

# passing X matrices values to the xtrain and xtest, decode ingone for erroring utf message error



Xtrain
#sparse mean that matrix has a lot of 0

#crate the model, train it, and get score


model=MultinomialNB()
model.fit(Xtrain, Ytrain)
print('train acc:', model.score(Xtrain, Ytrain))
print('test acc:', model.score(Xtest, Ytes))

Ptrain = model.predict(Xtrain)
Ptest = model.predict(Xtest)

print ('train_f1:' , f1_score(Ytrain, Ptrain))
print ('test_f1:', f1_score(Ytes, Ptest))

#check roc auc. Need proba function

Proba_train = model.predict_proba(Xtrain)[:,1]
Proba_test = model.predict_proba(Xtest)[:,1]

print ('train_ACU:' , roc_auc_score(Ytrain, Proba_train))
print ('test_AUC:', roc_auc_score(Ytes, Proba_test))

cm = confusion_matrix(Ytrain, Ptrain)
cm
#need confusion matrix, Ytrain, and the trained one at the first.

#for better visual lets plot CM

def plot_cm(cm):

  classes=['ham', 'spam']
  df_cm=pd.DataFrame(cm, index=classes, columns=classes)

  ax = sn.heatmap(df_cm, annot= True, fmt='g')

  ax.set_xlabel('Predicted')
  ax.set_ylabel('Target')

plot_cm(cm)

#plotting again CM via Sklearn

disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model.classes_)
disp.plot()

cm_test=confusion_matrix(Ytes, Ptest)
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm_test,display_labels=model.classes_)
disp2.plot()

#see words in spam or ham

def visualise(label):
  words=''

  for msg in df[df['labels']==label]['data']:
    msg=msg.lower()
    words+=msg+''


  wordcloud=WordCloud(width=600, height=400).generate(words)
  plt.imshow(wordcloud)
  plt.show()

visualise('spam')

visualise('ham')

X = featurizer.transform(df['data'])

df['predcitions']=model.predict(X)
df.head()

sneaky_spam = df[(df.predcitions==0) & (df.b_labels==1)]['data']

for msg in sneaky_spam:
  print(msg)

not_actually_spam = df[(df.predcitions==1) & (df.b_labels==0)]['data']

for msg in not_actually_spam:
  print(msg)
