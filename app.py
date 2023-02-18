from flask import Flask, request, jsonify
from scraping import get_all, get_article_sum

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    response = get_all(1)
    return jsonify({'data': response})


@app.route('/article', methods=['POST'])
def article():
    data = request.get_json()
    res = get_article_sum(data['url'], data['tipe'])
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
