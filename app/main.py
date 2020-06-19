from flask import Flask
import time

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    time.sleep(1)
    return '版本：v0.0.2'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
