# coding: utf-8

import os
from flask import Flask, request

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN', 'facebook_token')
bot = None


@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == os.environ.get('VERIFY_TOKEN', 'verify_token'):
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.generate_messaging_events(payload):
        print("Incoming from %s: %s" % (sender, message))

        response = bot.respond_to(message)

        print("Outgoing to %s: %s" % (sender, response))
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"

if __name__ == '__main__':
    bot = chatbot.Bot()
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
