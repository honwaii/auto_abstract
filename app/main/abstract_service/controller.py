#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime

from flask import Flask, render_template, request,url_for, send_from_directory, redirect
import json

from app.main.abstract_service import db
from app.main.abstract_service import service
# 视图层

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
  view_model=service.select_model(model_id)

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
  model["parameters"]={100}
  model["input"]=input_title
  model["output"]=output_abstract
  model["picture"]=output_tsne_fig
  response=service.insert_model(model)
  model_id=1

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
  model=service.select_model(model_id)
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