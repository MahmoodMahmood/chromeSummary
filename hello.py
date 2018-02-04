from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/data')
def data():
    #get requested url
    url = request.args.get('url')
    print(url)
    resp = Flask.Response(url)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    # return url