import json
import logging
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

app.run(host='127.0.0.1', port=1356, debug=DEBUG_MODE)