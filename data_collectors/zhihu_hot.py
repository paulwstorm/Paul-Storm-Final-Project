#!/usr/bin/env python
# coding: utf-8

# In[2]:


import webbrowser
import jieba
import jieba.posseg as pseg
jieba.enable_paddle()

import re
import pandas as pd
import datetime

import jieba
import jieba.posseg as pseg
import re

from bs4 import BeautifulSoup as bs4
import lxml
import requests

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from pymongo import MongoClient
from mongoengine import *

browser = webdriver.Chrome(executable_path='./chromedriver')


# In[3]:


browser.get("http://www.zhihu.com/")


# In[4]:


connect("weiboClozed")


# In[5]:


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


# In[6]:


level_1_chars = pd.read_csv("level_1_chars.csv", header=None)
level_1_chars = pd.Series(level_1_chars[0].array)

level_2_chars = pd.read_csv("level_2_chars.csv", header=None)
level_2_chars = pd.Series(level_2_chars[0].array)

level_3_chars = pd.read_csv("level_3_chars.csv", header=None)
level_3_chars = pd.Series(level_3_chars[0].array)

level_4_chars = pd.read_csv("level_4_chars.csv", header=None)
level_4_chars = pd.Series(level_4_chars[0].array)

level_5_chars = pd.read_csv("level_5_chars.csv", header=None)
level_5_chars = pd.Series(level_5_chars[0].array)

level_6_chars = pd.read_csv("level_6_chars.csv", header=None)
level_6_chars = pd.Series(level_6_chars[0].array)


# In[7]:


URL = "https://www.zhihu.com/"
browser.get(URL)


# In[8]:


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


# In[9]:


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


# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[13]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)

to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[14]:


time.sleep((1*60*30))


# In[15]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[16]:


time.sleep((1*60*60))


# In[17]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[18]:


time.sleep((1*60*60))


# In[19]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[20]:


time.sleep((1*60*60))


# In[21]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[22]:


time.sleep((1*60*60))


# In[23]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[24]:


time.sleep((1*60*60))


# In[25]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[26]:


time.sleep((1*60*60))


# In[27]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[28]:


time.sleep((1*60*60))


# In[29]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[30]:


time.sleep((1*60*60))


# In[31]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[32]:


time.sleep((1*60*60))


# In[33]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[34]:


time.sleep((1*60*60))


# In[35]:


URL = "https://www.zhihu.com/hot"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 1

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

hot_questions = []

hot_questions = []

for hot_item in bs_data.find_all('section',class_="HotItem"):
    hot_question = []
    
    image = hot_item.find("img")
    try:
        image_url = image['src']
    except:
        image_url = ""
        
    content = hot_item.find('div',class_="HotItem-content")
    url = content.find('a')['href']
    hot_question.append(url)
    hot_question.append(image_url)
    question_content = content.find('h2', class_="HotItem-title").text
    hot_question.append(question_content)
    try:
        full_text = content.find("p", class_="HotItem-excerpt HotItem-excerpt--multiLine").text
        hot_question.append(full_text)
    except:
        full_text = ""
        hot_question.append(full_text)
    hotness_level = content.find("div", class_="HotItem-metrics").text[:-2]
    hot_question.append(hotness_level)
    date_retrieved = datetime.datetime.now()
    hot_question.append(date_retrieved)
    hot_questions.append(hot_question)

hot_questions = pd.DataFrame(hot_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
hot_questions["source"] = "zhihu_hot"

hot_questions['tokenized_content'] = hot_questions['content'].apply(tokenized_content)
hot_questions['chars'] = hot_questions['content'].apply(question_chars)
hot_questions['words_pos'] = hot_questions['content'].apply(question_pos)
hot_questions['reading_level'] = hot_questions['chars'].apply(question_level)


to_drop = []

for index, row in hot_questions.iterrows():
    if (len(hot_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(hot_questions)
        
hot_questions = hot_questions.drop(to_drop)

len(hot_questions)

for index, row in hot_questions.iterrows():
    post = Post.objects(postContent = hot_questions.loc[index]['content']).update(
        set__postUrl = hot_questions.loc[index]['url'],
        set__postImageUrl = hot_questions.loc[index]['image_url'],
        set__postContent = hot_questions.loc[index]['content'],
        set__postTokenizedContent = hot_questions.loc[index]['tokenized_content'],
        set__postHeader = hot_questions.loc[index]['additional_content'],
        set__postPopularity = hot_questions.loc[index]['popularity'],
        set__dateRetrieved = hot_questions.loc[index]['date_retrieved'],
        set__postSource = hot_questions.loc[index]['source'],
        set__postChars = hot_questions.loc[index]['chars'],
        set__postWordsPos = hot_questions.loc[index]['words_pos'],
        set__postLevel = hot_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[ ]:




