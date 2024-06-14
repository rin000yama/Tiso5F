from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient, Configuration, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import (
    FollowEvent, MessageEvent, PostbackEvent, TextMessageContent
)
import os
import json
import database


file = open("info.json", "r")
info = json.load(file)


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = info["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = info["YOUR_CHANNEL_SECRET"]


app = Flask(__name__)


configuration = Configuration(access_token=YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


# ここでデータベースを初期化し起動
database.function.init_db()


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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):


    # ここで送られてきた内容をデータベースに保存
    user_id = event.source.user_id
    message_text = event.message.text
    database.function.save_message(user_id, message_text)


    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )




# versionが古買った際のコード ###########################################################################################
# line_bot_api = v3.Client(channel_access_token=YOUR_CHANNEL_ACCESS_TOKEN)
# handler = v3.WebhookParser(channel_secret=YOUR_CHANNEL_SECRET)


# # ここでデータベースを初期化し起動
# database.function.init_db()


# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):


#     # ここで送られてきた内容をデータベースに保存
#     user_id = event.source.user_id
#     message_text = event.message.text
#     database.function.save_message(user_id, message_text)



#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
