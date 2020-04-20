#!/usr/bin/env python
# coding: utf-8

# In[1]:


from weibo import APIClient
import webbrowser
import jieba
import jieba.posseg as pseg
jieba.enable_paddle()

import re
import pandas as pd
import datetime

import time
from mongoengine import *


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


# In[6]:


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


# In[9]:


APP_KEY = '3654848948'
APP_SECRET = '1fd520170cc3980219b17156e65a9565'
CALLBACK_URL = 'http://api.weibo.com/oauth2/default.html'
 
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)


# In[10]:


url = client.get_authorize_url()
print(url)
webbrowser.open_new(url)


# In[11]:


print("输入url中code后面的内容后按回车键：")
code = 'ae5fd45d2e8f4b7994c96335d170bfd6'

r = client.request_access_token(code)


# In[ ]:


# 保存access_token, expires_in
access_token = r.access_token  # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in
# 设置得到的access_token，client可以直接调用API了
client.set_access_token(access_token, expires_in)
print(expires_in)


# In[ ]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

to_drop = []

for index, row in weibo_posts.iterrows():
    if (len(weibo_posts.loc[index, 'chars']) == 0):
        to_drop.append(index)
        
len(weibo_posts)
        
weibo_posts = weibo_posts.drop(to_drop)

len(weibo_posts)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[14]:


time.sleep((1*60*30))


# In[15]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[16]:


time.sleep((1*60*60))


# In[17]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[18]:


time.sleep((1*60*30))


# In[19]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[20]:


time.sleep((1*60*30))


# In[21]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[22]:


time.sleep((1*60*30))


# In[23]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[24]:


time.sleep((1*60*60))


# In[25]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[26]:


time.sleep((1*60*30))


# In[27]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[28]:


time.sleep((1*60*30))


# In[29]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[30]:


time.sleep((1*60*60))


# In[31]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[32]:


time.sleep((1*60*30))


# In[33]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[34]:


time.sleep((1*60*30))


# In[35]:


pub_timeline = client.get.statuses__home_timeline(count=100)

weibo_posts = []

for post in pub_timeline.statuses:
    if(post["user"]["insecurity"]["sexual_content"] == False):
        weibo_post = []

        url = ""

        try:
            image_url = post.bmiddle_pic
        except:
            image_url = ""

        content = post['text']
        header = ""
        user = post.user.screen_name
        user_image = post.user.profile_image_url
        user_url = post.user.profile_url
        popularity = post.attitudes_count
        popularity = "likes " + str(popularity)
        date_retrieved = datetime.datetime.now()
        
        weibo_post.append(url)
        weibo_post.append(image_url)
        weibo_post.append(content)
        weibo_post.append(header)
        weibo_post.append(user)
        weibo_post.append(user_image)
        weibo_post.append(user_url)
        weibo_post.append(popularity)
        weibo_post.append(date_retrieved)
        weibo_posts.append(weibo_post)
        
weibo_posts = pd.DataFrame(weibo_posts,columns=["url", "image_url", "content","additional_content","user","user_image","user_url","popularity","date_retrieved"])
weibo_posts["source"] = "weibo"

weibo_posts['tokenized_content'] = weibo_posts['content'].apply(tokenized_content)
weibo_posts['chars'] = weibo_posts['content'].apply(question_chars)
weibo_posts['words_pos'] = weibo_posts['content'].apply(question_pos)
weibo_posts['reading_level'] = weibo_posts['chars'].apply(question_level)

for index, row in weibo_posts.iterrows():
    post = Post.objects(postContent = weibo_posts.loc[index]['content']).update(
        set__postUrl = weibo_posts.loc[index]['url'],
        set__postImageUrl = weibo_posts.loc[index]['image_url'],
        set__postContent = weibo_posts.loc[index]['content'],
        set__postTokenizedContent = weibo_posts.loc[index]['tokenized_content'],
        set__postHeader = weibo_posts.loc[index]['additional_content'],
        set__postPopularity = weibo_posts.loc[index]['popularity'],
        set__dateRetrieved = weibo_posts.loc[index]['date_retrieved'],
        set__postSource = weibo_posts.loc[index]['source'],
        set__postChars = weibo_posts.loc[index]['chars'],
        set__postWordsPos = weibo_posts.loc[index]['words_pos'],
        set__postLevel = weibo_posts.loc[index]['reading_level'],
        set__postUser = weibo_posts.loc[index]['user'],
        set__postUserImageUrl = weibo_posts.loc[index]['user_image'],
        set__postUserUrl = weibo_posts.loc[index]['user_url'],
        upsert = True
    )
       


# In[ ]:




