from dotenv import load_dotenv
import os
from page_analyzer.validate import validator
from page_analyzer.parser import normalize_url
from page_analyzer.db_manager import DBManager
from page_analyzer.scraper import request_to_url
from page_analyzer.html_parser import parse_html_content
from flask import (Flask,
                   render_template,
                   redirect, request,
                   url_for, flash,
                   get_flashed_messages)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


db_manager = DBManager()
db_manager.create_tables()


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form['url']
    normal_url = normalize_url(url)
    correct_url = validator(normal_url)

    if not correct_url:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    url_id, url_exists = db_manager.add_url(normal_url)

    if url_exists:
        flash("Cтраница уже существует", "info")
    else:
        flash("Cтраница успешно добавлена", "success")

    return redirect(url_for('get_url', url_id=url_id)), 302


@app.route('/urls')
def get_urls():
    all_urls = db_manager.get_all_urls()
    return render_template('urls.html', urls_data=all_urls)


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    messages = get_flashed_messages(with_categories=True)
    url = db_manager.get_url_by_id(url_id)
    data_checks = db_manager.get_check_url(url_id)
    return render_template('url.html', url=url,
                           messages=messages, data=data_checks)


@app.post('/urls/<id>/checks')
def add_check_url(id):
    url = request.form['url']
    status_code, text = request_to_url(url)
    if status_code is None:
        flash('Произошла ошибка при проверке', 'danger')
        messages = get_flashed_messages(with_categories=True)
        url_data = db_manager.get_url_by_id(id)
        return render_template('url.html', url=url_data, messages=messages), 422
    website_data = parse_html_content(text)
    db_manager.add_check((id, status_code, *website_data))
    flash('Cтраница успешно проверена', 'success')
    return redirect(url_for('get_url', url_id=id))


@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html'), 404
