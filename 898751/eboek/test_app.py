# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from flask import Flask, render_template
from dropboxwsgi.dropboxwsgi import make_app MemoryCredStorage

app = Flask(__name__)

cfg = {
    'consumer_key': '2h6yjvi6od40yml',
    'consumer_secret': 'y2e8qqsjc5q7st8',
    'access_type': 'app_folder'
}


@app.route('/')
def index():


