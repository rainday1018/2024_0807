from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage  #傳輸回line官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent,     #傳輸過來的方法
    TextMessageContent  #使用者傳過來的資料格式
)
import os,sys
app = Flask(__name__)

configuration = Configuration(access_token='LINE_BOT_TOKEN')
handler = WebhookHandler('LINE_BOT_SECRET_KEY' , None)

#設計一個 callblack 的路由，提供給line官方後台去呼叫
#也就是所謂的呼叫 Webhook server
#因為官方會把使用者傳輸的訊息轉傳給 Webhook server
#所以會使用 RESTful API 的 POST 方法
@app.route("/callback", methods=['POST'])
def callback():
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

    return 'OK'

#根據不同的使用者事件(event)，用不同的方式回應
#eg.MessengeEvent 代表使用者單純傳訊息的事件
#TextMessengeContent 代表使用者傳輸的訊息內容是文字
#符合兩個條件的事件，會被handle_message所處理
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()