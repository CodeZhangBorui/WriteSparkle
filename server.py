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

@app.route('/api/subsequent/new', methods=['POST'])
def new_subsequent():
    result = geetest.verify_test(
        lot_number=request.form['lot_number'],
        captcha_output=request.form['captcha_output'],
        pass_token=request.form['pass_token'],
        gen_time=request.form['gen_time']
    )
    if result['result'] == 'success':
        # Generate GPT
        composition = request.form['composition']
        try:
            gptres = 'We have not implemented this feature yet. Please wait for the next update.'
        except:
            return json.dumps({
                'status': 'error',
                'message': '请求 ChatGPT 时出错。'
            })
        # Upload to database
        try:
            sid = str(uuid.uuid4())
            conn = sqlite3.connect('gpt4com.sqlite')
            c = conn.cursor()
            c.execute('INSERT INTO subsequent (sid, composition, gptres) VALUES (?, ?, ?)', (sid, composition, gptres))
            c.close()
            conn.commit()
            conn.close()
            logging.info(f"Add new composition {sid} to database.")
        except:
            return json.dumps({
                'status': 'error',
                'message': '请求数据库时出错。'
            })
        # Redirect
        return json.dumps({
            'status': 'success',
            'redirect': f'/subsequent/{sid}'
        })
    elif result['result'] == 'fail':
        return json.dumps({
            'status': 'error',
            'message': result['reason']
        })
    else:
        console.print_exception(result['exception'])
        return json.dumps({
            'status': 'error',
            'message': result['reason']
        })

@app.route('/subsequent/<sid>')
def get_subsequent(sid):
    conn = sqlite3.connect('gpt4com.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM subsequent WHERE sid = ?', (sid,))
    res = c.fetchone()
    c.close()
    conn.close()
    if res is None:
        return render_template('error.html', message="未找到这篇作文：SID 无效"), 404
    composition = res[1]
    gptres = res[2]
    return render_template('subsequent_result.html', sid=sid, composition=composition, gptres=gptres)

app.run(host='127.0.0.1', port=1356, debug=DEBUG_MODE)