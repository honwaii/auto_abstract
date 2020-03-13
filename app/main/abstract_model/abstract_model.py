#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import jieba
import gensim
import numpy as np

from typing import List
from functools import reduce
from gensim.models import KeyedVectors
from gensim.models.word2vec import Word2Vec
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA
from app.main.abstract_model.domain.abstract import Abstract
from app.main.abstract_model.domain.sentence import Sentence
from app.main.abstract_model.domain.word import Word
from app.main.common.cfg_operator import configuration
import sys

sys.path.append('E:\\NLPproject\\auto_abstract')


def load_word_vector_model(path=None) -> Word2Vec:
    """ 加载已训练的词向量模型
    Returns
    -------
        加载的模型
    """
    if path is None:
        path = configuration.get_config('word_vector_model_path')
    print("加载的词向量的路径: " + path)
    # 加载word2vec模型: 保存的形式为二进制
    word_embedding = gensim.models.Word2Vec.load(path)
    # 加载glove转换的模型: 保存的为文本形式
    # model = KeyedVectors.load_word2vec_format(word_vector_model_path)
    return word_embedding


def get_word_vector(word: str, feature_size: int, word_vector_model: Word2Vec):
    """ 获取某个词的词向量.

     Parameters
     ----------
     word : str
         需要查询词向量的词.
     feature_size: int
         词向量的维度.
     word_vector_model: Word2Vec
          加载的词向量量模型
     Returns
     -------
     out : ndarray
            某个词的词向量，未找到某个词的词向量时，返回为零向量.

     """
    try:
        word_vector = word_vector_model[word]
    except KeyError:
        word_vector = np.zeros(feature_size)
    return word_vector


def get_word_frequency(word_text, look_table):
    if word_text in look_table:
        return look_table[word_text]
    else:
        return 1.0


def sentence_to_vec(sentence_list: List[Sentence], feature_size: int, look_table: dict, a=1e-3):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(feature_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text, look_table))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector
            # 找不到某个词的情况下，会出现得到的词向量为0
            # if np.sum(vs) == 0:
            #     temp = np.ones(embedding_size)
            #     vs = np.add(temp, np.multiply(a_value, word.vector))
            #     print(word.text)
        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    # pca = PCA(n_components=embedding_size)
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < feature_size:
        for i in range(feature_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))
    return sentence_vecs


def get_all_sentences(sentences: list, feature_size: int, word_vector_model: Word2Vec):
    sentence_list = []
    for sentence in sentences:
        sentence = jieba.cut(sentence)
        word_list = []
        for word in sentence:
            vector = get_word_vector(word, feature_size, word_vector_model)
            word_list.append(Word(word, vector))
        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_list.append(Sentence(word_list))
    return sentence_list


def get_sentences_vector(contents: str, word_embedding: Word2Vec, word_frequency_dict: dict):
    sentences = get_content_sentences(contents)
    split_sentences_list = get_all_sentences(sentences, word_embedding.vector_size, word_embedding)
    sentence_vectors = sentence_to_vec(split_sentences_list, word_embedding.vector_size, word_frequency_dict)
    sentence_vector_lookup = combine_sentences_vector(sentence_vectors, sentences)
    return sentence_vector_lookup, sentences


def combine_sentences_vector(sentence_vectors, sentences):
    sentence_vector_lookup = dict()
    if len(sentence_vectors) == len(sentences):
        for i in range(len(sentence_vectors)):
            # map: text of the sentence -> vector
            sentence_vector_lookup[sentences[i].__str__()] = sentence_vectors[i]
    return sentence_vector_lookup


def get_words_frequency_dict():
    frequency_file = configuration.get_config('frequency_file')
    print("load word frequency file.")
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


def get_content_vector(contents: list, word_embedding: Word2Vec, word_frequency_dict: dict):
    sentences = get_all_sentences(contents, word_embedding.vector_size, word_embedding)
    sentence_vectors = sentence_to_vec(sentences, word_embedding.vector_size, word_frequency_dict)
    return sentence_vectors


def get_most_similar_sentences(top_num: int, sentence_vector_lookup: dict, title_content_vector, sentences: list,
                               coefficient: float):
    similar_sentences = {}
    for sen, vector in sentence_vector_lookup.items():
        # weighted_vector = get_knn_vector(sen, distance, sentence_vector_lookup, sentences)
        essay_vector = coefficient * title_content_vector[0] + (1 - coefficient) * title_content_vector[1]
        similarity = cosine(vector, essay_vector)
        similar_sentences[sen] = similarity
    sorted_list = sorted(similar_sentences, key=lambda sen: similar_sentences[sen])
    most_similar_sens = sorted_list[:top_num]

    indexes = []
    top_sentences_with_similarity = []
    for each in most_similar_sens:
        indexes.append(sentences.index(each))
        top_sentences_with_similarity.append((each, 1 - similar_sentences[each]))
    indexes = sorted(indexes)
    result = []

    for i in indexes:
        result.append(sentences[i])
    return result, top_sentences_with_similarity


def cosine(vec1, vec2):
    distance = pdist(np.vstack([vec1, vec2]), 'cosine')[0]
    return distance


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


def summarise(title: str, content: str) -> Abstract:
    if len(title.strip()) <= 0:
        abstract = '请正确填写文章和标题.'
        return Abstract(abstract, 0, [(abstract, 0)])
    if len(content) < 10:
        return Abstract(content, 1, [(content, 1)])

    word_embedding = load_word_vector_model()
    word_frequency_dict = get_words_frequency_dict()
    result = get_abstract(title, content, word_embedding, word_frequency_dict, 10, 0.5)
    print(result.similarity)
    print(result.abstract)
    return result


def get_abstract(title: str, content: str, word_embedding: Word2Vec, word_frequency_dict: dict, top_num: int,
                 coefficient: float) -> Abstract:
    if len(title.strip()) <= 0:
        abstract = '请正确填写文章和标题.'
        return Abstract(abstract, 0, [(abstract, 0)])
    if len(content.strip()) < 10:
        return Abstract(content, 1, [(content, 1)])
    try:
        print('compute sentences vector')
        sentence_vectors_lookup, sentences = get_sentences_vector(content, word_embedding, word_frequency_dict)
        print('compute title and content vector...')
        title_content_vector = get_content_vector([title, content], word_embedding, word_frequency_dict)
        print('find most similar sentences:')
        most_similar_sens, top_sentences_with_similarity = get_most_similar_sentences(top_num, sentence_vectors_lookup,
                                                                                      title_content_vector, sentences,
                                                                                      coefficient)
    except Exception:
        return Abstract(None, None, None)
        # print(most_similar_sens)
    most_similar_sens = get_nearby_sentences(1, most_similar_sens, sentences)

    result_similarity = 0
    if len(most_similar_sens) > 0:
        abstracted_content = reduce(lambda x, y: x + ', ' + y, most_similar_sens) + "。"
        result_vector = get_content_vector([title, content, abstracted_content], word_embedding, word_frequency_dict)
        result_similarity = 1 - cosine(result_vector[1], result_vector[2])
        print("摘要与全文的相似度:" + str(result_similarity))
    else:
        abstracted_content = "文章内容不合适."
    result = Abstract(abstracted_content, result_similarity, top_sentences_with_similarity)
    return result


def get_nearby_sentences(distance: int, most_similar_sens: list, sentences: list) -> list:
    temp = []
    for sen in most_similar_sens:
        last_sentences = []
        # 只选取添加一些连词， 其他无关的句子不选取
        for i in range(distance):
            index = sentences.index(sen)
            if index - 1 - i < 0:
                continue
            last_sentence = sentences[index - 1 - i]
            if len(last_sentence) < 3:
                last_sentences.append(last_sentence)

        last_sentences.reverse()
        last_sentences.append(sen)
        temp += last_sentences

    # # 去重
    nearby_sentences = []
    for sen in temp:
        if sen not in nearby_sentences:
            nearby_sentences.append(sen)
    return nearby_sentences


def test():
    with open("data/news.txt", encoding='utf-8') as file:
        lines = file.readlines()
        contents = ""
        for line in lines:
            contents += line.replace("\n", "")
        file.close()
        title = "钟南山院士团队联合研发咽拭子采样智能机器人取得阶段性进展"
        result = summarise(title, contents)
        # print(result)
        # print(result.similarity)
        # print(result.top_sentences)

# embedding_size = 100
# coefficient = 0.5
# top_num = 10
# test()
# s = None
# print(len(s))
