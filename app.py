from flask import Flask
from flask import request
from flask import jsonify
import sentiment

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/sentiment", methods=["POST"])
def senti():
    text = request.json
    avg_sentiment = sentiment.get_average_sentiment(text)
    return jsonify(avg_sentiment)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')