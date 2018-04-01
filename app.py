from flask import Flask
from flask import request
from flask import jsonify
import sentiment
from twilio.rest import Client

app = Flask(__name__)

account = 'ACc89d674cfce611bdb7ec2482511428d8'
token = 'c9a1c5ef2ff95d8eed2f82a55fef9681'
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
    text = request.data
    message = client.messages.create(to="+12132040146", from_="+12134087788",
                                     body=text)
    return text

@app.route('/h3')
def get_stored_sent():
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')
