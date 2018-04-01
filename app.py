from flask import Flask
from flask import request
from google.cloud import language

language_client = language.Client()

app = Flask(__name__)
language_client = language.Client()

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/sentiment", methods=["POST"])
def sentiment():
    text = request.json['text']
    document = language_client.document_from_html(text)
    print(text)
    return text

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')