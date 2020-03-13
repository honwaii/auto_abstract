#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 0012 21:16
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : model_trainning.py
import linecache
import re
from functools import reduce

import numpy as np
import pandas as pd

from app.main.abstract_model import abstract_model
from app.main.abstract_model.domain.essay import Essay
from app.main.abstract_service import service
from app.main.common.cfg_operator import configuration


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
    content = pd.read_csv(path, encoding='gb18030', usecols=['content'], iterator=True)
    index = 0
    chunk_size = 20
    chunks = []
    loop = True
    while loop:
        try:
            chunk = content.get_chunk(chunk_size)
            start_index = index * chunk_size
            for i in range(chunk.size):
                essay = chunk.at[start_index + i, "content"]
                # chunks.append(chunk.at[start_index + i, "content"])
                if isinstance(essay, str):
                    # sentences = cut_sentences(essay)
                    save_sentence([essay])
            index += 1
            if index == 2:
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


embedding_size = 100


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
    contents = pd.read_csv(essays_path, encoding='gb18030', usecols=['content', 'title'])
    essays = []
    for each in contents.iterrows():
        content = each[1]['content']
        title = each[1]['title']
        if title is None or not isinstance(title, str):
            title = ''
        if content is None or not isinstance(content, str):
            content = ''
        essay = Essay(title=title, content=content)
        essays.append(essay)
    return essays


def find_most_suitable_model():
    coefficient_init = 0.0
    # 获取每个模型的参数
    models = []
    # for num in range(50, 500, 50):
    #     model_name = 'word_embedding_model_' + str(num)
    num = 100
    # model_path = './model/' + model_name
    model_path = './model/wiki_xinwen_wordvector.model'
    word_embedding = abstract_model.load_word_vector_model(model_path)
    essays_list = get_essays()
    word_frequency_dict = abstract_model.get_words_frequency_dict()
    for top_num in range(5, 10, 1):
        for coefficient in np.arange(0, 1.0, 0.01):
            similarities = []
            result = {'word_embedding_feature': num, 'top_num': top_num, 'coefficients': coefficient}
            for essay in essays_list:
                abstract = abstract_model.get_abstract(title=essay.title, content=essay.content,
                                                       word_embedding=word_embedding,
                                                       word_frequency_dict=word_frequency_dict,
                                                       top_num=top_num,
                                                       coefficient=coefficient)
                # model = Model(num, top_num, coefficient, abstract)
                if abstract.similarity is not None:
                    similarities.append(abstract.similarity)
                else:
                    print('异常文章和内容: ')
                    print(essay.title)
                    print(essay.content)
                # if len(similarities) == 5:
                #     break
            exception = np.mean(similarities)
            var = np.var(similarities)
            result['exceptions'] = exception
            result['variances'] = var
            service.insert_model_training_data(result)
    return


find_most_suitable_model()
# embedding_size = 100
# essays = get_essays()
# handle_essay2sentences()
