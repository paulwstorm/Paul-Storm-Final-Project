#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import jieba
import jieba.posseg as pseg
jieba.enable_paddle()

import re
import pandas as pd
import datetime

import time
from mongoengine import *
import requests


# In[36]:


connect( db='heroku_1xm0ffdd', username='paul_storm', password='H$Krazy2020', host='mongodb://paul_storm:H$Krazy2020@ds231387.mlab.com:31387/heroku_1xm0ffdd' )

# In[28]:


class Post(Document):
    postUrl = StringField()
    postImageUrl = StringField()
    postContent = StringField()
    postTokenizedContent = ListField()
    postHeader = StringField()
    postUser = StringField()
    postUserImageUrl = StringField()
    postUserUrl = StringField()
    postPopularity = StringField()
    dateRetrieved = DateTimeField()
    postSource = StringField()
    postChars = ListField()
    postWordsPos = ListField()
    postLevel = IntField()
    meta = { "collection": "posts"}


# In[29]:


level_1_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_1_chars.csv', header=None)
level_1_chars = pd.Series(level_1_chars[0].array)

level_2_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_2_chars.csv', header=None)
level_2_chars = pd.Series(level_2_chars[0].array)

level_3_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_3_chars.csv', header=None)
level_3_chars = pd.Series(level_3_chars[0].array)

level_4_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_4_chars.csv', header=None)
level_4_chars = pd.Series(level_4_chars[0].array)

level_5_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_5_chars.csv', header=None)
level_5_chars = pd.Series(level_5_chars[0].array)

level_6_chars = pd.read_csv('https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/add_char_files/server/char_lists/level_6_chars.csv', header=None)
level_6_chars = pd.Series(level_6_chars[0].array)


# In[39]:


def tokenized_content(question):
    post = question
    words = pseg.cut(post)
    not_allowed = ["x", "eng"]
    regexp = re.compile(r'[.]')
    
    new_post = ""

    for word, flag in words:
        if ((flag not in not_allowed) and (regexp.search(word) == None)):
            new_post = new_post + word
                
    paddle_words = pseg.cut(new_post, use_paddle=True)
    
    tokenized_content = []
    
    for word, flag in paddle_words:
        tokenized_content.append([word,flag])
        
    return tokenized_content

def question_pos(question):
    post = question
    words = pseg.cut(post)
    not_allowed = ["x", "eng"]
    regexp = re.compile(r'[.]')
    
    new_post = ""

    for word, flag in words:
        if ((flag not in not_allowed) and (regexp.search(word) == None)):
            new_post = new_post + word
                
    paddle_words = pseg.cut(new_post, use_paddle=True)
    
    words_pos = []
    
    for word, flag in paddle_words:
        if(flag[0].isupper() == False):
            words_pos.append([word, flag])
    
    return words_pos

def question_chars(question):
    post = question
    words = pseg.cut(post)
    not_allowed = ["x", "eng"]
    regexp = re.compile(r'[0-9.]')
    
    new_post = ""

    for word, flag in words:
        if ((flag not in not_allowed) and (regexp.search(word) == None)):
            new_post = new_post + word
                
    paddle_words = pseg.cut(new_post, use_paddle=True)
    
    test_words = []

    for word, flag in paddle_words:
        if(flag[0].isupper() == False and flag[0] != "t"):
            test_words.append(word)
            
    chars = []
            
    for i in range(len(test_words)):
        for j in range(len(test_words[i])):
            chars.append(test_words[i][j])
            
    chars = pd.Series(chars)
    chars = chars.drop_duplicates()
    chars = chars.array
    
    return chars

def question_level(chars):
    hsk_level = 0
    
    if (len(level_1_chars[level_1_chars.isin(chars)]) == len(chars)):
        hsk_level = 1
    elif ((len(level_1_chars[level_1_chars.isin(chars)]) + 
           len(level_2_chars[level_2_chars.isin(chars)])) == len(chars)):
        hsk_level = 2
    elif ((len(level_1_chars[level_1_chars.isin(chars)]) + 
           len(level_2_chars[level_2_chars.isin(chars)]) +
           len(level_3_chars[level_3_chars.isin(chars)])) == len(chars)):
        hsk_level = 3
    elif ((len(level_1_chars[level_1_chars.isin(chars)]) + 
           len(level_2_chars[level_2_chars.isin(chars)]) +
           len(level_3_chars[level_3_chars.isin(chars)]) +
           len(level_4_chars[level_4_chars.isin(chars)])) == len(chars)):
        hsk_level = 4
    elif ((len(level_1_chars[level_1_chars.isin(chars)]) + 
           len(level_2_chars[level_2_chars.isin(chars)]) +
           len(level_3_chars[level_3_chars.isin(chars)]) +
           len(level_4_chars[level_4_chars.isin(chars)]) +
           len(level_5_chars[level_5_chars.isin(chars)])) == len(chars)):
        hsk_level = 5
    elif ((len(level_1_chars[level_1_chars.isin(chars)]) + 
           len(level_2_chars[level_2_chars.isin(chars)]) +
           len(level_3_chars[level_3_chars.isin(chars)]) +
           len(level_4_chars[level_4_chars.isin(chars)]) +
           len(level_5_chars[level_5_chars.isin(chars)]) +
           len(level_6_chars[level_6_chars.isin(chars)])) == len(chars)):
        hsk_level = 6
    else:
        hsk_level = 7
        
    return hsk_level


# In[40]:


response = requests.get("https://www.jsanai.com/api/selfnews/newslist")

headlines = []

for headline in response.json()['data']:
    new_headline = []
    url = "https://www.toutiao.com"
    image_url = headline['headpic']
    content = headline['title']
    date_retrieved = datetime.datetime.now()
    source = "toutiao"
    
    new_headline.append(url)
    new_headline.append(image_url)
    new_headline.append(content)
    new_headline.append(date_retrieved)
    new_headline.append(source)
    
    headlines.append(new_headline)

headlines = pd.DataFrame(headlines, columns=["url", "image_url", "content", "date_retrieved", "source"])

headlines['tokenized_content'] = headlines['content'].apply(tokenized_content)
headlines['chars'] = headlines['content'].apply(question_chars)
headlines['words_pos'] = headlines['content'].apply(question_pos)
headlines['reading_level'] = headlines['chars'].apply(question_level)

to_drop = []

for index, row in headlines.iterrows():
    if (len(headlines.loc[index, 'chars']) == 0):
        to_drop.append(index)
                
headlines = headlines.drop(to_drop)


# In[41]:


headlines


# In[43]:


for index, row in headlines.iterrows():
    post = Post.objects(postContent = headlines.loc[index]['content']).update(
        set__postUrl = headlines.loc[index]['url'],
        set__postImageUrl = headlines.loc[index]['image_url'],
        set__postContent = headlines.loc[index]['content'],
        set__postTokenizedContent = headlines.loc[index]['tokenized_content'],
        set__postHeader = "",
        set__postPopularity = "",
        set__dateRetrieved = headlines.loc[index]['date_retrieved'],
        set__postSource = headlines.loc[index]['source'],
        set__postChars = headlines.loc[index]['chars'],
        set__postWordsPos = headlines.loc[index]['words_pos'],
        set__postLevel = headlines.loc[index]['reading_level'],
        set__postUser = "",
        set__postUserImageUrl = "",
        set__postUserUrl = "",
        upsert = True
    )


# In[ ]:




