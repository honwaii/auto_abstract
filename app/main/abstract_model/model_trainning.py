#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 0012 21:16
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : model_trainning.py
import re
import linecache
import numpy as np
import pandas as pd
from functools import reduce
from app.main.common.cfg_operator import configuration

from app.main.abstract_model import abstract_model


def get_sentences(start: int, size: int, is_all: bool):
    path = configuration.get_config("processed_sentences")
    if is_all:
        with open(path, encoding='utf-8') as reader:
            sentences_all = reader.read().split("\n")
            sentences = []
            for sen in sentences_all:
                if len(sen) > 0:
                    sentences.append(sen)
            return sentences
    sentences = []
    if start < 0 or size <= 0:
        print("参数错误请检查,start={}, size={}", start, size)
        return sentences
    linecache.clearcache()
    for index in range(size):
        sen = linecache.getline(path, start + index)
        if len(sen.strip()) > 1:
            sentences.append(sen.replace("\n", ""))
    return sentences


def handle_essay2sentences():
    # 0. 从文件读取句子
    # Columns: [id, author, result, content, feature, title, url]
    path = configuration.get_config('sentences_path')
    content = pd.read_csv(path, encoding='gb18030', usecols=['content', 'title'], iterator=True)
    index = 0
    chunk_size = 15
    chunks = []
    loop = True
    while loop:
        try:
            chunk = content.get_chunk(chunk_size)
            # start_index = index * chunk_size
            for i in range(chunk.size):
                print(len(chunk['title']))
                print(len(chunk['content']))
                title =chunk['title'][i]
                essay = chunk['content'][i]
                # essay = chunk.at[start_index + i, "content"]
                # title = chunk.at[start_index + i, "title"]
                # chunks.append(chunk.at[start_index + i, "content"])
                # if isinstance(essay, str):
                # sentences = cut_sentences(essay)
                # save_sentence(sentences)
                print('title:'+title)
                print('content:'+str(essay).strip())
            index += 1
            if index == 2:
                print('ok')
                break
        except StopIteration:
            print("read finish.")
            loop = False
    sentences_temp = []
    for chunk in chunks:
        sentences_temp += str(chunk).split("。")
    sentences = []
    for sentence in sentences_temp:
        s = sentence.split("，")
        sentences += s
    return sentences


def cut_sentences(contents: str):
    contents = contents.replace("\n", "").strip()
    contents = contents.replace("\t", "").strip()
    contents = contents.replace("\r", "").strip()
    regex = r"[？！。?!【】,，;；……]"
    sentences_list = re.split(regex, contents)
    sentences = []
    for index in range(len(sentences_list)):
        s = sentences_list[index]
        sen_1 = re.subn(r"@(.*)：", "", s)[0].strip()
        sen_2 = re.subn(r"\s", "", sen_1)[0].strip()
        sen = re.subn(r"(（.*）)", "", sen_2)[0].strip()
        if len(sen) <= 1 or len(sen.strip()) <= 1:
            continue
        if index == len(sentences_list) - 1:
            sentences.append(sen)
        else:
            sentences.append(sen + '\r')
    return sentences


def save_sentence(sentences: list):
    path = configuration.get_config("processed_sentences")
    output = open(path, 'a+', encoding='utf-8')
    output.writelines(sentences)
    output.close()


def save_sentences_embedding(sentences: list, embedding: list):
    path = configuration.get_config('embedding_path')
    output = open(path, 'w')
    lines = []
    for s, vector in zip(sentences, embedding):
        vector_str = reduce(lambda x, y: str(x) + " " + str(y), vector)
        lines.append(s + " " + vector_str + "\r")
    output.writelines(lines)
    output.close()
    return


def get_knn_vector(sentence: str, distance: int, sentence_vector_lookup: dict, sentences: list):
    vector = sentence_vector_lookup[sentence]
    if distance <= 0:
        return vector

    for i in range(distance):
        index = sentences.index(sentence)
        if index - 1 - i > 0:
            last_sentence = sentences[index - 1 - i]
            last_sentence_vector = sentence_vector_lookup[last_sentence]
        else:
            last_sentence_vector = np.zeros(embedding_size)

        if index + 1 + i < len(sentences) - 1:
            next_sentence = sentences[index + i + 1]
            next_sentence_vector = sentence_vector_lookup[next_sentence]
        else:
            next_sentence_vector = np.zeros(embedding_size)

        vector = vector * 0.7 + last_sentence_vector * 0.15 + next_sentence_vector * 0.15
        return vector


def optimize(title_vector, content_vector):
    # 计算每个句子和文章的相似度时，需考虑标题和内容的权重
    # 文章和标题的句向量, 假设title和内容是线性相关的，则 vector = alpha * title + (1 - alpha) * content + b
    dw = title_vector - content_vector
    db = 1
    # w = w - learning_rate * dw
    # b = b - learning_rate * db
    return


def get_essays():
    essays_path = configuration.get_config('essays_path')
    contents = pd.read_csv(essays_path, encoding='gb18030', usecols=['content', 'title'], nrows=10000)
    print(contents.describe())
    for each in contents.iterrows():

        break
    return


def find_most_suitable_model():
    coefficient_init = 0.0

    for num in range(50, 500, 50):
        model_name = 'word_embedding_model_' + str(num)
        model_path = './model/' + model_name
        model = abstract_model.load_word_vector_model(model_path)

    return


embedding_size = 100
# get_essays()
handle_essay2sentences()