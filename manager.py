#!/usr/bin/env python3

from flask import Flask, render_template, flash, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap 
from app import create_app

from app.models import MCA

app = create_app('default')

manager = Manager(app)

testURL = '/home/bentley/mca_test'

@app.route('/')
def index():
    mca = MCA(testURL)

    return render_template('index.html',filename=mca.dbfilename, data_directory=mca.data_directory)

if __name__ == '__main__':
    manager.run()