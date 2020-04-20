#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


connect("weiboClozed")


# In[3]:


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


# In[4]:


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


# In[5]:


URL = "https://www.zhihu.com/"
browser.get(URL)


# In[6]:


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


# In[7]:


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


# In[8]:


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


# In[9]:


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


# In[10]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['tokenized_content'] = recommended_questions['content'].apply(tokenized_content)
recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postTokenizedContent = recommended_questions.loc[index]['tokenized_content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[11]:


time.sleep((1*60*30))


# In[12]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[13]:


time.sleep((1*60*30))


# In[14]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[15]:


time.sleep((1*60*30))


# In[16]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

to_drop = []

for index, row in recommended_questions.iterrows():
    if (len(recommended_questions.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[17]:


time.sleep((1*60*30))


# In[18]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[19]:


time.sleep((1*60*30))


# In[20]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[21]:


time.sleep((1*60*30))


# In[22]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[23]:


time.sleep((1*60*60))


# In[24]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[25]:


time.sleep((1*60*30))


# In[26]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[27]:


time.sleep((1*60*60))


# In[28]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[29]:


time.sleep((1*60*30))


# In[30]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[31]:


time.sleep((1*60*60))


# In[32]:


URL = "https://www.zhihu.com"
browser.get(URL)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

scrolldowns = 9

while scrolldowns:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scrolldowns -= 1

source_data = browser.page_source

bs_data = bs4(source_data, 'lxml')

recommended_questions = []

bs_data

for content in bs_data.find_all('div', class_="ContentItem AnswerItem"):
    recommended_question = []
    image = content.find('meta',itemprop="image")
    try:
        image_url = image["content"]
    except:
        image_url = ""
        
    question_url = content.find('meta')['content']
    question_content = content.find("h2", class_="ContentItem-title").text
    question_head = content.find("span", class_="RichText ztext CopyrightRichText-richText").text
    upvotes = content.find("button", class_="Button VoteButton VoteButton--up").text
                
    date_retrieved = datetime.datetime.now()
    
    recommended_question.append(question_url)
    recommended_question.append(image_url)
    recommended_question.append(question_content)
    recommended_question.append(question_head)
    recommended_question.append(upvotes)
    recommended_question.append(date_retrieved)
    
    recommended_questions.append(recommended_question)    

recommended_questions = pd.DataFrame(recommended_questions,columns=["url", "image_url", "content","additional_content","popularity","date_retrieved"])
recommended_questions["source"] = "zhihu_recommended"

recommended_questions['chars'] = recommended_questions['content'].apply(question_chars)
recommended_questions['words_pos'] = recommended_questions['content'].apply(question_pos)
recommended_questions['reading_level'] = recommended_questions['chars'].apply(question_level)

len(recommended_questions)
        
recommended_questions = recommended_questions.drop(to_drop)

len(recommended_questions)

for index, row in recommended_questions.iterrows():
    post = Post.objects(postContent = recommended_questions.loc[index]['content']).update(
        set__postUrl = recommended_questions.loc[index]['url'],
        set__postImageUrl = recommended_questions.loc[index]['image_url'],
        set__postContent = recommended_questions.loc[index]['content'],
        set__postHeader = recommended_questions.loc[index]['additional_content'],
        set__postPopularity = recommended_questions.loc[index]['popularity'],
        set__dateRetrieved = recommended_questions.loc[index]['date_retrieved'],
        set__postSource = recommended_questions.loc[index]['source'],
        set__postChars = recommended_questions.loc[index]['chars'],
        set__postWordsPos = recommended_questions.loc[index]['words_pos'],
        set__postLevel = recommended_questions.loc[index]['reading_level'],
        upsert = True
    )


# In[ ]:




