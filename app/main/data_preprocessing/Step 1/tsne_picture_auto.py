import matplotlib.pyplot as plt
from gensim.models import word2vec
from sklearn.manifold import TSNE
import random
import sys
import gensim

def tsne_plot(model, word_num):
    "Creates and TSNE model and plots it"
    for pth in range(1, 11):
        labels = []
        tokens = []
        total_size = len(model.wv.vocab)
        probability = word_num * 1.0/total_size
        for word in model.wv.vocab:
            r = random.random()
            if r <= probability:
                tokens.append(model[word])
                labels.append(word)

        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])

        plt.figure(figsize=(16, 16))
        for i in range(len(x)):
            plt.scatter(x[i] ,y[i])
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        # plt.show()
        plt.savefig(str(pth)+".png", dpi=300)
        plt.close()
if __name__ == "__main__":
    print(sys.platform)
    if sys.platform.startswith("win"):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    else:
        plt.rcParams['font.sans-serif'] = ['STFangsong']
        plt.rcParams['axes.unicode_minus'] = False
    input_word_vector_path = sys.argv[1]
    model = gensim.models.Word2Vec.load(input_word_vector_path)
    word_num = 200
    if len(sys.argv)>2:
        word_num = int(sys.argv[2])
    tsne_plot(model, word_num)
