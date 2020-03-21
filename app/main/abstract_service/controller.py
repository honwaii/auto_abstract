#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math

from flask import Flask, render_template, request, url_for, redirect

from app.main.abstract_service import service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# 自动摘要输入页面
@app.route("/auto_abs")
def auto_abs():
    return render_template("auto_abs.html")


@app.route("/auto_abs_error/<message>")
def error_auto_abs(message=None):
    return render_template("auto_abs.html", message=message)


@app.route("/show_auto_abs_result/<history_id>")
def show_auto_abs_result(history_id):
    history = service.select_history_byid(history_id)
    view_model = {
        "title": history["title"],
        "content": history["content"],
        "abstract": history["abstract"],
        "similarity": json.loads(history["top_sentences"]),
        "timestamp": history["timestamp"],
    }
    model_id = history["model_id"]

    return render_template("auto_abs_result.html", model=view_model)


@app.route("/mostsim_words/")
def most_similar_words():
    return render_template("most_similar_words.html")


@app.route("/error_mostsim_words/<message>")
def error_most_similar_words(message=None):
    return render_template("most_similar_words.html", message=message)


@app.route("/mostsim_words/<word>")
def show_most_similar_words(word):
    print("show_most_similar_words")
    tsne_fig_name = gen_tsne_fig_name(word)
    tsne_fig_path = "./static/" + tsne_fig_name
    result = get_most_similar_words(word=word, output_pic_path=tsne_fig_path)
    if result:
        return render_template("most_similar_words.html", word=word, ms_words=result, tsne_fig=tsne_fig_path)
    else:
        message = "sorry~暂时没有关于\"" + word + "\"的资料。"
        print(message)
        return redirect(url_for('error_most_similar_words', message=message))


@app.route("/history")
def history():
    return redirect(url_for('history_page', page=1))


@app.route("/history/<page>")
def history_page(page=1):
    page = int(page)
    history_number_in_a_page = 8
    histories = service.select_history_all()
    # print(type(histories), type(len(histories)))
    page_num = math.ceil(int(len(histories)) / history_number_in_a_page)
    start_id = (page - 1) * history_number_in_a_page + 1
    if page == page_num:
        histories = histories[start_id - 1:]
    else:
        histories = histories[start_id - 1:start_id + 7]
    # print(histories)

    return render_template("history.html", histories=histories, page=page, page_num=page_num)


# 提交输入数据
@app.route("/submit_input", methods=["POST"])
def submit_input():
    print(request.form)
    title = request.form.get("input_title")
    content = request.form.get("input_content")
    if title == "" or content == "":
        message = "请正确输入标题与内容。"
        return redirect(url_for('error_auto_abs', message=message))
    # 调用模型接口
    else:
        abstract = service.get_abstract_result(title, content)

        history = {}
        history["title"] = title
        history["content"] = content
        history["abstract"] = abstract.abstract
        history["top_sentences"] = abstract.top_sentences
        history["similarity"] = abstract.similarity
        history["model_id"] = 158
        response = service.insert_history(history)
        print(response)
        if response != 0:
            history_id = response
            return redirect(url_for('show_auto_abs_result', history_id=history_id))
        else:
            message = "不好意思，出了点问题，请再次提交。"
            return redirect(url_for('error_auto_abs', message=message))


@app.route("/submit_word", methods=["POST"])
def submit_word():
    print(request.form)
    input_word = request.form.get("input_word")
    if input_word == "":
        message = "请输入词语"
        return redirect(url_for('error_most_similar_words', message=message))
    else:
        return redirect(url_for('show_most_similar_words', word=input_word))


# hard code
def get_output(input_title: str, input_sentence: str):
    model_id = str(1)
    similarity = {"作为全球最大口罩生产国": 4, "我国出口的口罩占据着海外市场将近50%的供应": 3, }

    output = {
        "abstract": "作为全球最大口罩生产国，我国出口的口罩占据着海外市场将近50%的供应",
        "similarity": json.dumps(similarity),
        "model_id": model_id
    }

    return output


def get_tsne_fig(input_title: str, input_sentence: str):
    return "https://www.mathworks.com/help/examples/stats/win64/ChangeTsneSettingsExample_01.png"


def insert_or_update_models(model):
    model_id = "0"
    return ("success", model_id)


def get_most_similar_words(word, output_pic_path='./picture/tsne/tsne.png'):
    result = service.query_similarity(query_word=word, output_pic_path=output_pic_path)
    # print(type(result))
    return result


def gen_tsne_fig_name(word):
    fig = 'tsne.png'
    return fig


# hard code

if __name__ == "__main__":
    app.run(debug=True)
