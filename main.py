import urllib.request
import os
import sys
import json
import scrape as sc
from argparse import ArgumentParser
import pytz
import certifi
import requests
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import chromedriver_binary
import re
 
from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
 
app = Flask(__name__)
 
SECRET = os.environ("YOUR_CHANNEL_SECRET")
ACCESS_TOKEN = os.environ("YOUR_CHANNEL_ACCESS_TOKEN")

 
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)
 
 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
 
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
 
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
 
    word = event.message.text
    result = sc.getNews(word)
 
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=result)
    )
 
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
