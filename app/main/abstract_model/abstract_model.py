#!/usr/bin/python
# -*- coding: utf-8 -*-
import linecache
import re
from functools import reduce
from typing import List

import gensim
import jieba
import scipy
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from gensim.models.word2vec import Word2Vec
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA

from app.main.abstract_model.domain.sentence import Sentence
from app.main.abstract_model.domain.word import Word
from app.main.abstract_model.src import data_io, SIF_embedding, params
from app.main.abstract_model.src.params import params
from app.main.common.cfg_operator import configuration
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec


def load_word_vector_model():
    word_vector_model_path = configuration.get_config('word_vector_model_path')
    print(word_vector_model_path)
    # model = KeyedVectors.load_word2vec_format(word_vector_model_path)
    model = gensim.models.Word2Vec.load(word_vector_model_path)
    return model


def get_word_vector(word: str, embedding_size: int, word_vector_model: Word2Vec):
    try:
        word_vector = word_vector_model[word]
    except KeyError:
        word_vector = np.zeros(embedding_size)
    return word_vector


def get_sif_embedding():
    word_file = configuration.get_config('word_file')  # word vector file, can be downloaded from GloVe website
    # word_file = "./data/sgns.wiki.word"  # word vector file, can be downloaded from GloVe website
    frequency_file = configuration.get_config('frequency_file')  # each line is a word and its frequency
    # weight_file = './auxiliary_data/SogouLabDic.dic'  # each line is a word and its frequency
    # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
    weight_para = float(configuration.get_config('weight_para'))
    rmpc = 1  # number of principal components to remove in SIF weighting scheme
    # sentences = ['this is an example sentence', 'this is another sentence that is slightly longer']
    sentences = get_sentences(0, 100, True)
    # save_sentence(sentences)

    # load word vectors 1. 加载词向量文件
    print("1. 加载词向量文件")
    (words, We) = data_io.getWordmap(word_file)
    # load word weights  2. 加载权重文件
    print("2. 加载词频文件")
    word2weight = data_io.getWordWeight(frequency_file,
                                        weight_para)  # word2weight['str'] is the weight for the word 'str'
    # print(word2weight)
    #  3. 计算词向量文件中，每个词所对应的权重
    print("3. 计算权重")
    weight4ind = data_io.getWeight(words, word2weight)  # weight4ind[i] is the weight for the i-th word
    # load sentences
    # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
    #  4. x : 词的索引  m：表示所在位置是否有一个词
    print("4. 建立索引")
    x, m = data_io.sentences2idx(sentences, words)
    #  5. 得到各句话中各个词对应的权重的矩阵
    print("5. 计算权重矩阵")
    w = data_io.seq2weight(x, m, weight4ind)  # get word weights
    # set parameters
    params.rmpc = rmpc

    # get SIF embedding
    print("6. 得到句子向量")
    embedding = SIF_embedding.SIF_embedding(We, x, w, params)  # embedding[i,:] is the embedding for sentence i
    return sentences, embedding


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
                    sentences = cut_sentences(essay)
                    save_sentence(sentences)
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


def get_word_frequency(word_text, look_table):
    if word_text in look_table:
        return look_table[word_text]
    else:
        return 1.0


def sentence_to_vec(sentence_list: List[Sentence], embedding_size: int, look_table: dict, a=1e-3):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text, look_table))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector
        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    # pca = PCA(n_components=embedding_size)
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))
    return sentence_vecs


def get_all_sentences(sentences: list, embedding_size: int, word_vector_model: Word2Vec):
    sentence_list = []
    for sentence in sentences:
        sentence = jieba.cut(sentence)
        word_list = []
        for word in sentence:
            vector = get_word_vector(word, embedding_size, word_vector_model)
            word_list.append(Word(word, vector))
        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_list.append(Sentence(word_list))
    return sentence_list


def get_sentences_vector(contents: str):
    model = load_word_vector_model()
    # sentences = get_sentences(0, 300, True)
    sentences = get_content_sentences(contents)
    split_sentences_list = get_all_sentences(sentences, embedding_size, model)
    word_frequency_dict = get_words_frequency_dict()
    sentence_vectors = sentence_to_vec(split_sentences_list, embedding_size, word_frequency_dict)
    sentence_vector_lookup = combine_sentences_vector(sentence_vectors, sentences)
    return sentence_vector_lookup


def combine_sentences_vector(sentence_vectors, sentences):
    sentence_vector_lookup = dict()
    if len(sentence_vectors) == len(sentences):
        for i in range(len(sentence_vectors)):
            # map: text of the sentence -> vector
            sentence_vector_lookup[sentences[i].__str__()] = sentence_vectors[i]
    return sentence_vector_lookup


def get_words_frequency_dict():
    frequency_file = configuration.get_config('frequency_file')
    word2weight = {}
    with open(frequency_file, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if len(line) <= 0:
            continue
        line = line.split()
        if len(line) == 2:
            word2weight[line[0]] = float(line[1])
        else:
            print(line)
    return word2weight


# print(model['的'])
# print(t)


def glove_to_word2vec():
    glove_vector_model_path = configuration.get_config('glove_vector_model_path')
    print(glove_vector_model_path)
    word_vector_model_path = configuration.get_config('word_vector_model_path')
    print(word_vector_model_path)
    # 输入文件
    glove_file = datapath(glove_vector_model_path)
    # 输出文件
    tmp_file = get_tmpfile(word_vector_model_path)
    # 开始转换
    glove2word2vec(glove_file, tmp_file)
    print('finish')


# glove_to_word2vec()
# 加载转化后的文件


def get_content_vector(content: str):
    model = load_word_vector_model()
    sentences = get_all_sentences([content], embedding_size, model)
    word_frequency_dict = get_words_frequency_dict()
    sentence_vectors = sentence_to_vec(sentences, embedding_size, word_frequency_dict)
    return sentence_vectors


def get_most_similar_sentences(top_num: int, sentence_vector_lookup: dict, content_vector):
    similar_sentences = {}
    for sen, vector in sentence_vector_lookup.items():
        similarity = cosine(vector, content_vector)
        similar_sentences[sen] = similarity
    sorted_list = sorted(similar_sentences, key=lambda sen: similar_sentences[sen])
    return sorted_list[:top_num]


def cosine(vec1, vec2):
    distance = pdist(np.vstack([vec1, vec2]), 'cosine')[0]
    return distance


def knn_smooth():
    return


def get_content_sentences(contents: str):
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
        sentences.append(sen)
    return sentences


def test():
    with open("./data/new.txt", encoding='utf-8') as file:
        contents = str(file.readlines()).replace("\n", "")
        file.close()
        print('compute sentences vector')
        sentence_vectors_lookup = get_sentences_vector(contents)
        print('compute content vector.')
        content_vector = get_content_vector(contents)
        print('find most similar sentences:')
        most_similar_sens = get_most_similar_sentences(10, sentence_vectors_lookup, content_vector)
        print(most_similar_sens)


# embedding_size = 100
# handle_essay2sentences()
# s, em = get_sif_embedding()
# save_sentences_embedding(s, em)
# model = load_word_vector_model()

embedding_size = 100

# t = get_sentences_vector()
# with open("./data/temp.txt", 'a+', encoding="utf-8") as file:
#     for i in t:
#         file.writelines(str(i))
#     file.close()
# print('ok')
