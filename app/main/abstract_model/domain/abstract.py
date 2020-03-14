#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 0012 22:20
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : abstract.py


class Abstract:
    def __init__(self, abstract: str, similarity: float, top_sentences: dict):
        self.abstract = abstract
        self.similarity = similarity
        self.top_sentences = top_sentences

