from flask import Flask, render_template
import os
import json

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static'
    )

BOOKS = ['The War-Torn Kingdom', 'Cities of Gold and Glory']
CHARACTER_PATH = "characters"


@app.route('/')
def root():
    return render_template("home.html.jinja")


@app.route('/load')
def load():
    chars = {}
    for i in range(len(BOOKS)):
        i = i + 1
        files = os.listdir(f'{CHARACTER_PATH}/Book{i}')
        chars[i] = []
        for file in files:
            with open(f'{CHARACTER_PATH}/Book{i}/{file}') as f:
                c = json.loads(f.read())['character']
                d = {
                    'name': c['name'],
                    'profession': c['profession'],
                    'abilities': c['abilities'],
                    'image': file.replace('.json', '.png')
                }
                chars[i].append(d)
    return render_template("load.html.jinja", characters=chars, books=BOOKS)


if __name__ == "__main__":
    """
    Main entrypoint

    Launches the flask app when run with "python app.py"

    Args
    - None

    Returns
    - None
    """
    app.run()
