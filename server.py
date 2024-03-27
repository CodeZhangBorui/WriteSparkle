#-- coding:UTF-8 --
import json
import datetime
import logging
import uuid
import sqlite3

import requests

import geetest

from flask import Flask, request, redirect, session, render_template, send_file, Response

from rich.logging import RichHandler
from rich.console import Console

from openai import OpenAI

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

with open('types.json', 'r') as f:
    prompts = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']

client = OpenAI(
    base_url=config['openai']['base_url'],
    api_key=config['openai']['api_key']
)

# Print boot information
logging.info("Starting WriteSparkle:")
logging.info("  - Geetest ID: " + config['geetest']['captcha_id'])
logging.info("  - OpenAI API Key: " + config['openai']['api_key'][:16] + "...")
logging.info("  - OpenAI Model: " + config['openai']['model'])
logging.info("  - OpenAI Base URL: " + config['openai']['base_url'])
logging.info("  - Number of Loaded Prompts: " + str(len(prompts)))

@app.route('/')
def index():
    products = []
    for key in prompts:
        products.append({
            'name': prompts[key]['name'],
            'description': prompts[key]['description'],
            'id': key
        })
    return render_template('index.html', products=products)

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def errorhandler_404(e):
    return render_template('error.html', code=404, message="404 Not Found"), 404

@app.errorhandler(500)
def errorhandler_500(e):
    return render_template('error.html', code=500, message="500 Internal Server Error"), 500

@app.route('/create/<type>')
def create(type):
    try:
        ptype = prompts[type]
    except KeyError:
        return render_template('error.html', message=f"无效的作文类型：{type}"), 404
    return render_template('create.html', captcha_id=config['geetest']['captcha_id'], type=ptype, typeid=type)


@app.route('/api/create/<type>', methods=['POST'])
def new_passage(type):
    result = geetest.verify_test(
        lot_number=request.json['captcha']['lot_number'],
        captcha_output=request.json['captcha']['captcha_output'],
        pass_token=request.json['captcha']['pass_token'],
        gen_time=request.json['captcha']['gen_time']
    )
    if result['result'] == 'success':
        # Generate GPT
        prompt = prompts[type]
        composition = request.json['composition']
        try:
            completion = client.chat.completions.create(
                model='gpt-4',
                messages=[
                    {
                        "role": "system",
                        "content": prompt['system']
                    },
                    {
                        "role": "user",
                        "content": composition
                    }
                ]
            )
            generateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            message = completion.choices[0].message.content
        except:
            console.print_exception()
            return json.dumps({
                'status': 'error',
                'message': '请求 ChatGPT 时出错。'
            })
        # Upload to database
        try:
            sid = str(uuid.uuid4())
            conn = sqlite3.connect('wsparkle.sqlite')
            c = conn.cursor()
            c.execute('INSERT INTO passage (sid, type, composition, message) VALUES (?, ?, ?, ?)', (sid, type, composition, message))
            c.close()
            conn.commit()
            conn.close()
            logging.info(f"Add new composition {sid} to database.")
        except:
            console.print_exception()
            return json.dumps({
                'status': 'error',
                'message': '请求数据库时出错。'
            })
        # Redirect
        return json.dumps({
            'status': 'success',
            'redirect': f'/passage/{sid}'
        })
    elif result['result'] == 'fail':
        return json.dumps({
            'status': 'error',
            'message': result['reason']
        })
    else:
        console.print_exception()
        return json.dumps({
            'status': 'error',
            'message': result['reason']
        })

@app.route('/passage/<sid>')
def get_passage(sid):
    conn = sqlite3.connect('wsparkle.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM passage WHERE sid = ?', (sid,))
    res = c.fetchone()
    c.close()
    conn.close()
    if res is None:
        return render_template('error.html', message="未找到这篇作文：SID 无效"), 404
    type = res[1]
    composition = res[2]
    gptres = res[3]
    return render_template(
        'passage_result.html',
        sid=sid,
        type=prompts[type],
        composition=composition.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>'),
        gptres=gptres.replace('\n', '<br>')
    )

app.run(host='127.0.0.1', port=1356, debug=DEBUG_MODE)
