#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,request,url_for, render_template

app = Flask(__name__)
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/autoabs")
def auto_abs():
  return render_template("auto_abs.html",current_language='English')

if __name__ == "__main__":
  app.run(debug=True)