#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 0015 12:00
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : model_generate.py
from datetime import datetime

import gensim
from gensim.test.utils import datapath
from gensim import utils


class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __init__(self, text_path):
        self.text_path = text_path

    def __iter__(self):
        corpus_path = datapath(self.text_path)
        for line in open(corpus_path, "r", encoding="utf-8"):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)


if __name__ == "__main__":
    input_text_path = r'E:\projects\2020\auto_abstract\app\main\data_preprocessing/wiki_xinwen_fengci.txt'
    for num in range(50, 500, 50):
        model_name = 'word_embedding_model_' + str(num)
        print('start model:' + model_name)
        start = datetime.now().timestamp()
        output_word_vector_path = 'E:\projects\\2020\\auto_abstract\\app\\main\\abstract_model\\model\\' + model_name
        sentences = MyCorpus(input_text_path)
        model = gensim.models.Word2Vec(sentences=sentences, size=num)
        model.save(output_word_vector_path)
        end = datetime.now().timestamp()
        print('耗时:' + str(end - start))
        print('finish model:' + model_name)
