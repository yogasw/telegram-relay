from flask import Flask
from os import environ
app = Flask(__name__)

HOST = '0.0.0.0'
PORT = int(environ.get('PORT', "8080"))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
