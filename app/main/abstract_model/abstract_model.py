#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from functools import reduce
import pandas as pd
import re

sys.path.append("./src")
from app.main.abstract_model.src import data_io, SIF_embedding, params
from app.main.abstract_model.src.params import params
from app.main.common.cfg_operator import configuration


def get_sif_embedding():
    word_file = configuration.get_config('word_file')  # word vector file, can be downloaded from GloVe website
    # word_file = "./data/sgns.wiki.word"  # word vector file, can be downloaded from GloVe website
    weight_file = configuration.get_config('weight_file')  # each line is a word and its frequency
    # weight_file = './auxiliary_data/SogouLabDic.dic'  # each line is a word and its frequency
    # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
    weight_para = float(configuration.get_config('weight_para'))
    rmpc = 1  # number of principal components to remove in SIF weighting scheme
    # sentences = ['this is an example sentence', 'this is another sentence that is slightly longer']
    sentences = get_sentences()
    # sentences = ["我喜欢你。", "你是一只小毛驴。"]

    # load word vectors 1. 加载词向量文件
    print("1. 加载词向量文件")
    (words, We) = data_io.getWordmap(word_file)
    # load word weights  2. 加载权重文件
    print("2. 加载权重文件")
    word2weight = data_io.getWordWeight(weight_file, weight_para)  # word2weight['str'] is the weight for the word 'str'
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


def get_sentences():
    # 0. 从文件读取句子
    # Columns: [id, author, result, content, feature, title, url]
    path = configuration.get_config('sentences_path')
    content = pd.read_csv(path, encoding='gb18030', usecols=['content'], iterator=True)
    index = 0
    chunk_size = 500
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
            # if index == 3:
            #     break
        except StopIteration:
            print("read finish.")
            loop = False
    # 1. 拆分句子，先按句号拆分，再按照逗号拆分
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
    lines = ''
    for s, vector in zip(sentences, embedding):
        vector_str = reduce(lambda x, y: str(x) + " " + str(y), vector)
        lines += (s + " " + vector_str + "\n")
    output.write(lines)
    output.close()
    return


def cut_sentences(contents: str):
    contents = contents.replace("\n", "").strip()
    regex = r"[？！。?!【】,，]"
    sentences_list = re.split(regex, contents)
    sentences = []
    for s in sentences_list:
        sen_1 = re.subn(r"@(.*)：", "", s)[0].strip()
        sen_2 = re.subn(r"\s", "", sen_1)[0].strip()
        sen = re.subn(r"(（.*）)", "", sen_2)[0].strip()
        # mini_sens = sen.split("，")
        # sentences += mini_sens
        sentences.append(sen + "\n")
    return sentences


def save_sentence(sentences: list):
    path = configuration.get_config("processed_sentences")
    output = open(path, 'a+', encoding='utf-8')
    output.writelines(sentences)
    output.write("\n")
    output.close()


get_sentences()
# s, em = get_sif_embedding()
# save_sentences_embedding(s, em)
