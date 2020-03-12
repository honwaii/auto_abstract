#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 0012 21:20
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : utils.py
from app.main.common.cfg_operator import configuration
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile


def glove_to_word2vec(input_path: str, output_path: str):
    """
    将glove类型的词向量模型转换为word2vec类型的词向量模型
    Parameters
    ----------
    input_path : str
        glove类型的词向量模型所在的文件路径.
    output_path: str
        转换为word2vec模型后的输出路径.

    Returns
    -------
        None
    """
    glove_file = datapath(input_path)
    word2vec_file = get_tmpfile(output_path)
    glove2word2vec(glove_file, word2vec_file)
    print('convert finished.')


def test():
    glove_vector_model_path = configuration.get_config('glove_vector_model_path')
    print(glove_vector_model_path)
    word_vector_model_path = configuration.get_config('word_vector_model_path')
    print(word_vector_model_path)
    glove_to_word2vec(glove_vector_model_path, word_vector_model_path)
