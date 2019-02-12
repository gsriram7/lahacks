from flask import Flask
from flask import request
from flask import jsonify
import sentiment
from twilio.rest import Client

app = Flask(__name__)

account = ''
token = ''
client = Client(account, token)

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/sentiment", methods=["POST"])
def senti():
    text = request.json
    print(text)
    avg_sentiment = sentiment.get_average_sentiment(text)
    return jsonify(avg_sentiment)

@app.route('/sms', methods=["POST"])
def sms():
    text = request.json
    company = text.get('company', 'EMPTY')
    user = text.get('user', 'EMPTY')
    number = text.get('number', '')
    message = 'Hi {}, {} stocks are not in a good shape, you might want to sell them quick'.format(user, company)
    sms = client.messages.create(to=number, from_="",
                                     body=message)
    return sms.status

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
