import sys
from lib.api import translate_api

from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/translate", methods=['POST'])
def translate():
    '''
    parse the source text from the request
    '''
    try:
        src_text = request.values.get('src_text')
        dst_text = translate_api(src_text)
        return dst_text
    except:
        print('Bad request. Try again...')

if __name__ == '__main__':
    app.run()
