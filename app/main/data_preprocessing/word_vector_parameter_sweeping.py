#-*- encoding=utf-8 -*-
import sys
import time

import gensim
from gensim import utils
from gensim.test.utils import datapath


class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __init__(self, text_path):
        self.text_path = text_path

    def __iter__(self):
        corpus_path = datapath(self.text_path)
        for line in open(corpus_path, "r", encoding="utf-8"):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)




def query_words(input_word_vector_path):
    """
    :param input_word_vector_path:
    :return:
    """
    model = gensim.models.Word2Vec.load(input_word_vector_path)
    actual_words = []
    actual_words.append("旅游")
    actual_words.append("北京")
    actual_words.append("奥巴马")
    actual_words.append("垃圾")   #添加这个的目的是在于我们的语料都是比较正规的语料，如果语料是从评论里面采集的应该有不同的效果
    print(actual_words)
    for word in actual_words:
        print("---------------------"+word+"-----------------------------")
        lst = model.most_similar(positive=[word], topn=10)
        for l in lst:
            print(l)


def explore_sg_cbow(input_text_path):
    print("\n\n开始探索sg=0和=1的影响")
    for sg in [0, 1]: #sg 如果sg = 1就用skipgram, 如果sg = 0就用cbow
        print("sg", sg)
        sentences = MyCorpus(input_text_path)
        model = gensim.models.Word2Vec(sentences=sentences, sg=sg)
        output_model_path = "./sg-"+str(sg) + ".model"
        model.save(output_model_path)
        query_words(output_model_path)

def explore_iter(input_text_path): #iter=5：訓練的回數，訓練過少會使得詞關係過為鬆散，訓練過度又會使得詞關係過為極端
    print("\n\n开始探索iter的影响，iter=5：訓練的回數，訓練過少會使得詞關係過為鬆散，訓練過度又會使得詞關係過為極端")
    for iter in [5, 10, 15]:
        print("iter", iter)
        sentences = MyCorpus(input_text_path)
        model = gensim.models.Word2Vec(sentences=sentences, iter=iter)
        output_model_path = "./iter-" + str(iter) + ".model"
        model.save(output_model_path)
        query_words(output_model_path)

def explore_workers(input_text_path):
    print("\n\n开始探索worker数量的影响")
    for worker in [1, 2, 4, 6, 8]:
        print("worker", worker)
        sentences = MyCorpus(input_text_path)
        t1 = time.time()
        model = gensim.models.Word2Vec(sentences=sentences, workers=worker)
        t2 = time.time()
        print("worker" + str(worker) +" training takes", t2-t1, "seconds")
        model.save("./worker-"+ str(worker) + ".model")

if __name__ == "__main__":
    input_text_path = sys.argv[1]
    explore_sg_cbow(input_text_path)
    explore_iter(input_text_path)
    explore_workers(input_text_path)
    # query_words("wiki_xinwen_wordvector.model")
