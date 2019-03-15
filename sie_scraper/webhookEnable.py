from flask import abort, Flask, redirect, render_template, request, session, url_for
import os
import time
import threading
import fileAutomation
import datetime

app = Flask(__name__)
APP_SECRET = 'qmevdx3rohasue5'

@app.route("/test")
def hello():
    return "Hello World!"

# @app.route('/webhookEnhanza', methods=['GET'])
# def challenge():
#     '''Respond to the webhook challenge (GET request) by echoing back the challenge parameter.'''
#     if request.method == "GET":
#         challenge1 = request.args.get('challenge')
#         #print "hello"
#         return challenge1#request.args.get('challenge')
#
#
#
# @app.route('/webhookEnhanzanew', methods=['POST'])
# def challenge1():
#     '''Respond to the webhook challenge (GET request) by echoing back the challenge parameter.'''
#     if request.method == "POST":
#         print("Hello")
#         #return " " #request.args.get('challenge')
#         return " "



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
