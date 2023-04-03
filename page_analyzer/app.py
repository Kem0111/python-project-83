from dotenv import load_dotenv
import os
import psycopg2
from page_analyzer.validate import validator
from page_analyzer.parser import normalize_url
from page_analyzer.db_manager import DBManager
from flask import (Flask,
                   render_template,
                   redirect, request,
                   url_for, flash,
                   get_flashed_messages)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
db_manager = DBManager(conn)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def add_url():
    url = request.form['url']
    normal_url = normalize_url(url)
    correct_url = validator(normal_url)

    if not correct_url:
        flash('Некорректный URL', 'error')
        return redirect(url_for('index'))

    url_id, url_exists = db_manager.add_url(normal_url)

    if url_exists:
        flash("Cтраница уже существует", "warning")
    else:
        flash("Cтраница успешно добавлена", "success")

    return redirect(url_for('url', url_id=url_id))


@app.route('/urls')
def urls():
    all_urls = db_manager.get_all_urls()
    return render_template('urls.html', urls=all_urls)


@app.route('/urls/<int:url_id>')
def url(url_id):
    messages = get_flashed_messages(with_categories=True)
    url = db_manager.get_url_by_id(url_id)
    return render_template('url.html', url=url, messages=messages)
