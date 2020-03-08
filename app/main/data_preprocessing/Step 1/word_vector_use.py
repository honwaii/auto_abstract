from gensim.test.utils import datapath
from gensim import utils
import sys
import gensim

def analogy(x1, x2, y1, model):
    return model.most_similar(positive=[y1, x2], negative=[x1])
if __name__ == "__main__":
    input_word_vector_path = sys.argv[1]
    model = gensim.models.Word2Vec.load(input_word_vector_path)
    while True:
        word = input("请输入要查询的词:")
        if word == "exit":
            break
        word = word.strip()
        if " " in word or " " in word:
            [x1, x2, y1] = word.split()
            lst = analogy(x1, x2, y1, model)
        else:
            lst = model.most_similar(positive=[word], topn=10)
        for l in lst:
            print(l)