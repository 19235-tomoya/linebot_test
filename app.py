#-*- coding: utf-8 -*-

# インポートするライブラリ
from flask import Flask, request, abort, render_template, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction,
    MessageTemplateAction, URITemplateAction, StickerMessage,
    URIAction, RichMenu, PostbackEvent
)

import os
import json


# ウェブアプリケーションフレームワーク:flaskの定義
app = Flask(__name__)

# サーバの環境変数から LINE_Access_Tokenを取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# サーバの環境変数から LINE_Channel_Secretを取得
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
handler = WebhookHandler(LINE_CHANNEL_SECRET)



# "/"にGETリクエストを送ると返す  (ルートのアドレスに以下のものを配置することを明言)
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot"



# LINE側が送ってきたメッセージが正しいか検証する
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # プログラムの通常の操作中に発生したイベントの報告
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名検証で失敗したときは例外をあげる
        abort(400)
    return jsonify({"state": 200})



# MessageEvent　テキストメッセージ受け取った時
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 受け取りデータの確認
    print(f"\nevent：{event}\n")

    # 受け取ったメッセージ
    text = event.message.text

    if "こんにちは" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello World")
         )
    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「" + text + "」って何？")
         )




if __name__ == "__main__":
    port = int(os.getenv("PORT",8080))
    app.run(host="0.0.0.0", port=port)
