# 业务逻辑层
import json
import pprint
import random
import time

import gensim
import matplotlib.pyplot as plt
from gensim.models import word2vec
from sklearn.manifold import TSNE

from app.main.abstract_model import abstract_model
from app.main.abstract_model.domain.abstract import Abstract
from app.main.abstract_service import db

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 插入历史
def insert_history(history):
    # 系统现在时间
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = """
            insert
            into
            auto_abstract_history(title, content, abstract, similarity, model_id, top_sentences, timestamp)
            values(%s, %s, %s, %s, %s, %s, %s)
    """
    insert_history_tuple = (
        history["title"], history["content"], history["abstract"], str(history["similarity"]), history["model_id"],
        json.dumps(history['top_sentences']), time_now)
    response = db.insert_with_param(sql, insert_history_tuple)
    return response[0][0]


# 按id查询历史
def select_history_byid(history_id):
    sql = "select * from auto_abstract_history where history_id = " + str(history_id)
    print(sql)
    history = db.query_data(sql)[0]
    return history


# 按查询参数模糊查询所有历史
def select_history(history: dict) -> list:
    sql = "select * from auto_abstract_history where title like %s and content like %s" \
          "and abstract like %s and similarity like %s and model_id like %s and timestamp like %s"
    # 处理无key情况
    if not history.__contains__("title"):
        history["title"] = ""

    if not history.__contains__("content"):
        history["content"] = ""

    if not history.__contains__("abstract"):
        history["abstract"] = ""

    if not history.__contains__("similarity"):
        history["similarity"] = ""

    if not history.__contains__("model_id"):
        history["model_id"] = ""

    if not history.__contains__("timestamp"):
        history["timestamp"] = ""

    title_like = "%" + history["title"] + "%"
    content_like = "%" + history["content"] + "%"
    abstract_like = "%" + history["abstract"] + "%"
    similarity = "%" + history["similarity"] + "%"
    model_id = "%" + history["model_id"] + "%"
    timestamp = "%" + history["timestamp"] + "%"

    select_history_list = [title_like, content_like, abstract_like, similarity, model_id, timestamp]
    histories = db.query_data_with_param(sql, select_history_list)
    return histories


def select_history_all():
    sql = "select * from auto_abstract_history"
    histories = db.query_data(sql)
    return histories


# 从数据库查出二进制数据写到硬盘./picture


# 插入model
def insert_model(model):
    # 系统现在时间
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    model["timestamp"] = time_now

    sql = """
            insert
            into
            auto_abstract_model(parameters, input, output, picture, timestamp)
            values(%s, %s, %s, %s, %s)
            """
    insert_model_tuple = (model["parameters"], model["input"], model["output"], model["picture"], model["timestamp"])
    print(sql)
    ret = db.insert_with_param(sql, insert_model_tuple)
    return ret


# 根据id查询model
def select_model(model_id):
    sql = "select * from auto_abstract_model where model_id = " + str(model_id)
    print(sql)
    model = db.query_data(sql)[0]
    return model


def store_picture():
    sql = """
        select input, picture from auto_abstract_model
        """
    data = db.query_data(sql)
    for datum in data:
        filename = datum["input"]
        pic = datum["picture"]
        print(type(pic))
        fw = open('./picture/' + filename + '.png', 'wb')
        fw.write(pic)
        fw.close
    print(len(data))
    print(data)


model = None


def init_wordvecs(word_vector_model_path):  # 初始化词向量模型
    model = gensim.models.Word2Vec.load(word_vector_model_path)
    return model


def async1(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async1
def tsne_plot(query_word, output_path, model, word_num=200):  # 画关于query_word的tsne图，这个query word 会被显示在图中
    # 图会被保存在output_path里面
    "Creates and TSNE model and plots it"
    for pth in range(1, 2):
        labels = []
        tokens = []
        total_size = len(model.wv.vocab)
        probability = word_num * 1.0 / total_size
        for word in model.wv.vocab:
            r = random.random()
            if r <= probability:
                tokens.append(model[word])
                labels.append(word)
        tokens.append(model[query_word])
        labels.append(query_word)
        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])

        plt.figure(figsize=(16, 16))
        for i in range(len(x)):
            plt.scatter(x[i], y[i])
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        # plt.show()
        plt.savefig(output_path, dpi=300)


import threading


def query_similarity(query_word, output_pic_path):
    """
    根据输入的query_word ，返回一个字符串，字符串包含和这个query_word最相似的10个词以及相似度，
    并且将这个query_word以及随机选取的200个单词用tsne画图，图片保存在output_pic_path里面
    :param query_word: 查询词
    :param output_pic_path: 输出的tsne图的地址
    :param model_path: 词向量模型的地址
    :return:
    """
    # if model is None:
    #     return "You should initialized the word_vector model first by calling init_wordvects"
    # else:
    try:
        lst = abstract_model.word_embedding.most_similar(positive=[query_word], topn=10)
        tsne_plot(query_word, output_pic_path, abstract_model.word_embedding, word_num=200)
    except:
        return False
    # print(dict(lst))
    return dict(lst)


def insert_model_training_data(model: dict):
    sql = """
            insert
            into
            auto_abstract_model(word_embedding_feature,top_num, coefficients, exceptions, variances,batch_size)
            values(%s, %s, %s, %s, %s, %s)
            """
    insert_model_tuple = (
        model["word_embedding_feature"], model["top_num"], str(model["coefficients"]), str(model["exceptions"]),
        str(model["variances"]), model['batch_size'])
    ret = db.insert_with_param(sql, insert_model_tuple)
    return ret


def get_abstract_result(title: str, content: str) -> Abstract:
    abstract = abstract_model.summarise(title, content)
    return abstract


def get_model_training_data(word_embedding_feature: int):
    sql = "select coefficients,exceptions,variances from auto_abstract_model where word_embedding_feature=" + str(
        word_embedding_feature) + " and top_num=8 and batch_size=1000"
    data = db.query_data(sql)
    return data


if __name__ == '__main__':
    history = {
        "title": "333",
    }
    histories = select_history(history)
    pprint.pprint(histories)
