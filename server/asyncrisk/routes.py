from asyncrisk import app
from flask import render_template


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')
