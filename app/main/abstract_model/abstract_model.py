#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.main.abstract_model.src import data_io, SIF_embedding, params
from app.main.abstract_model.src.params import params


def get_sif_embedding():
    wordfile = './data/sgns.wiki.word'  # word vector file, can be downloaded from GloVe website
    weightfile = './auxiliary_data/SogouLabDic.dic'  # each line is a word and its frequency
    weightpara = 1e-3  # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
    rmpc = 1  # number of principal components to remove in SIF weighting scheme
    # sentences = ['this is an example sentence', 'this is another sentence that is slightly longer']
    sentences = ['我今天真的很高兴！', '你住在什么地方。']

    # load word vectors 1. 加载词向量文件
    (words, We) = data_io.getWordmap(wordfile)
    # load word weights  2. 加载权重文件
    word2weight = data_io.getWordWeight(weightfile, weightpara)  # word2weight['str'] is the weight for the word 'str'
    #  3. 计算词向量文件中，每个词所对应的权重
    weight4ind = data_io.getWeight(words, word2weight)  # weight4ind[i] is the weight for the i-th word
    # load sentences
    # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
    #  4. x : 词的索引  m：表示所在位置是否有一个词
    x, m = data_io.sentences2idx(sentences, words)
    #  5. 得到各句话中各个词对应的权重的矩阵
    w = data_io.seq2weight(x, m, weight4ind)  # get word weights

    # set parameters
    params.rmpc = rmpc

    # get SIF embedding
    embedding = SIF_embedding.SIF_embedding(We, x, w, params)  # embedding[i,:] is the embedding for sentence i
    return embedding


get_sif_embedding()
