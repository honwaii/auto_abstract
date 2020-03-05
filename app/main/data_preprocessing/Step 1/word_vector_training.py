from gensim.test.utils import datapath
from gensim import utils
import sys
import gensim
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
    input_text_path = sys.argv[1]
    output_word_vector_path = sys.argv[2]
    sentences = MyCorpus(input_text_path)
    model = gensim.models.Word2Vec(sentences=sentences)
    model.save(output_word_vector_path)