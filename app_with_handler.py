# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort  ,render_template
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
import os,sys
from heandle_key import get_secret_and_token 
from opai0809 import  chat_with_chatgpt

app = Flask(__name__)
keys = get_secret_and_token()
handler = WebhookHandler(keys['LINE_BOT_SECRET_KEY'])
configuration = Configuration( access_token=keys['LINE_CHANNEL_ACCESS_TOKEN'])

@app.route("/")
def say_hello_world(username=""):
    return render_template("hello.html",name=username)

@app.route("/callback", methods=['POST'])
def callback():
    # 設計一個 #callback 的路由，提供給Line官方後台去呼叫
    # 也就所謂的呼叫Webhook Server
    # 因為官方會把使用者傳輸的訊息轉傳給Webhook Server
    # 所以會使用 RESTful API 的 POST 方法

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
        
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):

    user_message = event.message.text #使用者傳過來的訊息
    api_key = keys["OPENAI_API_KEY"]
    response = chat_with_chatgpt(user_message, api_key)
   
        
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )


if __name__ == "__main__":
    app.run(debug=True)