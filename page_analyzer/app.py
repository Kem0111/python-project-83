from dotenv import load_dotenv
import os
from page_analyzer.validate import validator
from page_analyzer.url_parser import normalize_url
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
    """Render the main page of the application."""

    return render_template('index.html')


@app.post('/urls')
def add_url():
    """
    Add URL to the database and redirect to the URL's details page.
    Display a message if the URL is invalid or already exists.
    """
    url = request.form['url']
    normal_url = normalize_url(url)
    correct_url = validator(normal_url)

    if not correct_url:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    url_id, url_exists = db_manager.add_url(normal_url)

    if url_exists:
        flash("Страница уже существует", "info")
    else:
        flash("Страница успешно добавлена", "success")

    return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls')
def get_urls():
    """
    Render a page displaying a list of all URLs
    and their check information.
    """

    all_urls = db_manager.get_all_urls()
    return render_template('urls.html', urls_data=all_urls)


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    """
    Render a page displaying detailed information about a specific URL
    and its check results.
    """
    messages = get_flashed_messages(with_categories=True)
    url = db_manager.get_url_by_id(url_id)
    data_checks = db_manager.get_check_url(url_id)
    return render_template('url.html', url=url,
                           messages=messages, data=data_checks)


@app.post('/urls/<id>/checks')
def add_check_url(id):
    """
    Perform a check on a specific URL and store the check results
    in the database.
    Redirect to the URL's details page and display a message
    if the check was successful.
    """
    url = request.form['url']
    status_code, text = request_to_url(url)
    print(status_code)

    if status_code is None:
        flash('Произошла ошибка при проверке', 'danger')
        messages = get_flashed_messages(with_categories=True)
        url_data = db_manager.get_url_by_id(id)
        return render_template('url.html', url=url_data, messages=messages), 422

    website_data = parse_html_content(text)
    db_manager.add_check((id, status_code, *website_data))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', url_id=id))


@app.errorhandler(404)
def page_not_found_error(error):
    """Render a custom 404 error page."""

    return render_template('error.html'), 404
