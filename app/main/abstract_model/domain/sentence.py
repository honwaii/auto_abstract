#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 0003 20:40
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : sentence.py


class Sentence:
    def __init__(self, word_list):
        self.word_list = word_list

    def len(self) -> int:
        return len(self.word_list)
