import json
import logging
import uuid
import sqlite3

import requests

import geetest

from flask import Flask, request, redirect, session, render_template

from rich.logging import RichHandler
from rich.console import Console

DEBUG_MODE = True

# Logging setup
logging.basicConfig(
    level="INFO",
    format="%(message)s", datefmt="[%X]", 
    handlers=[RichHandler()]
)

console = Console()

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'h546yjuk5tiyr4jt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subsequent')
def subsequent():
    return render_template('subsequent.html', captcha_id=config['geetest']['captcha_id'])

@app.route('/subsequent/new', methods=['POST'])
def new_subsequent():
    result = geetest.verify_test(
        lot_number=request.data['captcha']['lot_number'],
        captcha_output=request.data['captcha']['captcha_output'],
        pass_token=request.data['captcha']['pass_token'],
        gen_time=request.data['captcha']['gen_time']
    )
    if result['result'] == 'success':
        # Generate GPT
        composition = request.data['composition']
        gptres = ''
        # Upload to database
        sid = uuid.uuid4()
        conn = sqlite3.connect('gpt4com.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO subsequent (sid, composition, gptres) VALUES (?, ?)', (sid, composition, gptres))
        # Redirect
        return redirect(f'/subsequent/{sid}')
    elif result['result'] == 'fail':
        return result['reason']
    else:
        console.print_exception(result['exception'])
        return result['reason']

@app.route('/subsequent/<sid>')
def get_subsequent(sid):
    conn = sqlite3.connect('gpt4com.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM subsequent WHERE sid = ?', (sid,))
    res = c.fetchone()
    if res is None:
        return render_template('subsequent_notfound.html')
    composition = res[1]
    gptres = res[2]
    return render_template('subsequent_result.html', sid=sid, composition=composition, gptres=gptres)

app.run(host='127.0.0.1', port=1356, debug=DEBUG_MODE)