# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:39:49 2022
@author: Lien
"""
import pandas as pd
import jieba
from wordcloud import WordCloud
from collections import Counter

# build dictionary ad stop words
jieba.set_dictionary('dict.txt')
stop_words = []
with open('stop_word.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stop_words.append(data)
stop_words.append('paragraph')
stop_words.append('wp')
stop_words.append('xa0')
stop_words.append('n')
stop_words.append('t')
stop_words.append('位數')
stop_words.append('百分比')
stop_words.append('u3000')
stop_words.append('n2022')

df = pd.read_excel("result.xlsx")
words = ""

def stringToList(string):
    listRes = list(string.split(" "))
    return listRes

for i in range(df.shape[0]):
    if pd.isnull(df['Text'][i]):
        continue
    # Save words
    print('month:',str(int(df['Date'][i])))    
    word_list = jieba.cut(str(df['Text'][i]))
    word_list2 = []
    for word in word_list:
        if  (word not in stop_words) and word.isnumeric()!=1 and word!=' ' and len(word)>1:
            word_list2.append(word)
    words += " ".join(word_list2)
    # Produce word cloud
    if df['Company'][i]=='SUMCO':
        print('Produce word cloud for month ',str(int(df['Date'][i])))
        textlist = stringToList(words)
        counts = Counter(textlist)
        print(counts.most_common(5))
        print('\n')
        cloud = WordCloud(width=1000, height=500, collocations  =False, background_color='white',font_path='SourceHanSansTW-Regular.otf').generate(words)
        cloud.to_file('wordCloud'+str(int(df['Date'][i]))+'.png')
        words = ""