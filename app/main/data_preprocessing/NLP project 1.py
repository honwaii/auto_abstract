#!/usr/bin/env python
# coding: utf-8

# # Step1-1 维基百科中文语料的处理
# 
# 
# 使用WikiExtractor提取维基百科语料
# 
# WikiExtractor链接：https://github.com/attardi/wikiextractor
# 需要的环境官网有写明：The tool is written in Python and requires Python 2.7 or Python 3.3+ but no additional library.
# 意思是:基于python2.7或python3.3， 且不需要依赖于第三方模块。
# 安装GitHub，之后打开命令行：
# 
# git clone https://github.com/attardi/wikiextractor wikiextractor
# 
# cd wikiextractor
# 
# python setup.py install
# 
# 将语料的压缩文件拷贝进wikiextractor文件夹里面，接下来就是核心命令：
# 打开命令行：
# 
# cd wikiextractor
# 
# python WikiExtractor.py -b 1024M -o extracted zhwiki-20200201-pages-articles-multistream.xml.bz2

# # Step1-2: 汉语新闻语料库的处理

# In[13]:


# get_ipython().system('pip3 install gensim')

# In[1]:


import pandas as pd
import jieba
import re
from collections import Counter


def token(string):
    return re.findall('\w+', string)


# In[14]:


# 读取汉语新闻语料库文件
df = pd.read_csv('sqlResult_1558435.csv')
df.head()

# In[ ]:


import chardet

binary_data = open('sqlResult_1558435.csv', 'rb').read()
chardet.detect(binary_data)

TOKEN = []
df.fillna('', inplace=True)
articles = df['comment'].tolist()
print('number of articels: %d' % len(articles))
for i in range(len(articles)):
    if i % 10000 == 0: print(i)
    TOKEN += jieba.cut(''.join(token(articles[i])))

for i, line in enumerate((open('train.txt', encoding='utf8'))):
    if i % 1000 == 0: print(i)
    TOKEN += jieba.cut(''.join(token(line)))
