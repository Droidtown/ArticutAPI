#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: CS_chatbot_flask.py
# Development starting date: 2019.07.13
# Developer: Peter. w (peter.w@droidtown.co)

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chatbotDemo.html")
    #return render_template('index.html')

@app.route("/ask", methods=["POST"])
def bot():
    responseSTR = "RECEIVED:{}".format(request.values["inputSTR"])

    return responseSTR


if __name__ == "__main__":
    app.debug = True
    app.run()