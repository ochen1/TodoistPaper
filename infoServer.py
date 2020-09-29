from flask import Flask, request, render_template, send_from_directory
from time import time, strftime

from json import load as loadJSON

from math import ceil

app = Flask(__name__)


@app.route('/')
def main():
    with open('database.json', 'r') as f:
        db = loadJSON(f)
        start = request.args.get(
            'after',
            default=0,
            type=int
        )
        perpage = request.args.get(
            'perpage',
            default=8,
            type=int
        )
        end = min([
            start + perpage - 1,
            len(db['items'])
        ])
        litems = db['items'][start:end + 1]
        return render_template(
            "infoIndex.html",
            currTime=lambda: strftime("%c"),
            litems=litems,
            pagination={
                'page': round(start / perpage) + 1,
                'totalPages': ceil(perpage / len(db['items'])) + 2,
                'perpage': perpage,
                'first_page_url': '/?after=%i&perpage=%i' % (0, perpage),
                'last_page_url': '/?after=%i&perpage=%i' % (len(db['items']) - len(db['items']) % perpage, perpage),
                'prev_page_url': '/?after=%i&perpage=%i' % (max([0, start - perpage]), perpage),
                'next_page_url': '/?after=%i&perpage=%i' % (end + 1 if end + 1 < len(db['items']) else start, perpage)
            }
        )


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
