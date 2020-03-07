#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime

import xlwt
from flask import Flask, render_template, request,url_for, send_from_directory, redirect
import json

from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts

from app import db
from jinja2 import Markup
app = Flask(__name__)
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/auto_abs")
def auto_abs():
  return render_template("auto_abs.html")

@app.route("/show_auto_abs_result/<model_id>")
def show_auto_abs_result(model_id):
  '''
  sql = "select * from auto_abstract_model where model_id=" + model_id
  data = db.query_data(sql)
  model = data[0]
  '''
  view_model=get_model_from_db(model_id)

  return render_template("auto_abs_result.html",model=view_model)

@app.route("/history")
def history():
  histories=get_auto_abstract_history()
  return render_template("history.html",histories=histories)

@app.route("/algorithm_model")
def algorithm_model():
  return render_template("algorithm_model.html")




@app.route("/submit_input", methods=["POST"])
def submit_input():
  print(request.form)
  input_title=request.form.get("input_title")
  input_content=request.form.get("input_content")
  output_abstract=get_abstract(input_title,input_content)
  output_tsne_fig=get_tsne_fig(input_title,input_content)

  model={}
  model["model_id"]=None
  model["parameters"]={}
  model["input"]={"input_title":input_title,"input_content":input_content}
  model["output"]=output_abstract
  model["picture"]=output_tsne_fig
  model["timestamp"]=""
  model["commets"]=""
  (response,model_id)=insert_or_update_models(model)
  return redirect(url_for('show_auto_abs_result',model_id=model_id))



#hard code
def get_abstract(input_title:str,input_sentence:str):
  return "作为全球最大口罩生产国，我国出口的口罩占据着海外市场将近50%的供应"

def get_tsne_fig(input_title:str,input_sentence:str):
  return "https://www.mathworks.com/help/examples/stats/win64/ChangeTsneSettingsExample_01.png"

def insert_or_update_models(model):
  model_id="0"
  return ("success",model_id)

def get_model_from_db(model_id:str):
  model={}
  if model_id == "0":
    model["model_id"]="0"
    model["parameters"]={}
    model["input"]={"input_title":"全球公共卫生事件的不断蔓延"
                    ,"input_content":'''最近一段时间，由于全球公共卫生事件的不断蔓延，各国的医疗防护物资也纷纷“告急”，出现了供不应求的情况。与此同时，作为全球数一数二的医疗物资生产大国，我国在加速完成产能突破之际，也迅速做出了行动。据第一财经3月4日最新报道，我国工信部有关代表人士指出，中国是防护服生产的大国，我们鼓励国内防护服的生产企业积极对接国外需求，按相应标准规范生产出口，为全球共同抗击疫情做出贡献。据报道，该代表人士透露，在我国企业的努力生产下，目前防护服的生产供应已经能够满足医务人员的使用需求。其中，我国湖北地区每日供应的防护服数量达到了25万件，连续十几天出现了供大于求的情况。除了鼓励防护服出口至海外，部分口罩生产企业也开始寻求来自海外的订单。中国基金报的一则报道指出，近日新野纺织称，该司的纺织产品可以用于口罩生产，可以少量出口至越南。另一家口罩生产商奥佳华在一个互动平台称，该公司生产的专业抗菌口罩已经开始上线，可以出口至北美、东南亚、日本等国家。数据显示，2月29日，全国口罩日产能达到1.1亿只，日产量达到1.16亿只。
  在我国的口罩产能取得全新突破下，恐怕还不能就此松懈。作为全球最大口罩生产国，我国出口的口罩占据着海外市场将近50%的供应，其中，美国市场有90%的口罩就依赖中国供应。2月28日当天，美国还打算通过运用“特殊权力”'''}
    model["output"]="作为全球最大口罩生产国，我国出口的口罩占据着海外市场将近50%的供应"
    model["picture"]="https://www.mathworks.com/help/examples/stats/win64/ChangeTsneSettingsExample_01.png"
    model["timestamp"]=""
    model["commets"]=""
  else:
    model["model_id"]=str(model_id)
    model["parameters"]={}
    model["input"]={"input_title":"TitleTitleTitleTitle",
                    "input_content":"ContentContentContentContent"}
  return model

def get_auto_abstract_history():
  histories=[
              {
              "history_id":0,
              "title":"0000000000000000",
              "content":"ContentContentContentContentContentContent",
              "timestamp":"timestamp",
              "model_id":0
              },
              {
              "history_id":1,
              "title":"111111111111111",
              "content":"ContentContentContentContentContentContent",
              "timestamp":"timestamp",
              "model_id":1
              },
              {
              "history_id":2,
              "title":"2222222222222222",
              "content":"ContentContentContentContentContentContent",
              "timestamp":"timestamp",
              "model_id":2
              }]
  print(history)
  return histories
#hard code

if __name__ == "__main__":
  app.run(debug=True)