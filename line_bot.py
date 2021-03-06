# 必須import line 的SDK(software development kit軟體開發套件)才能寫程式與line互動, SDK是由軟體公司提供
# flask, django為python主流架設伺服器與網站的套件

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('UgFjUyMHgNmgR2CLIfy9RRSg4+kWBkIqdmVugis+CvXHvhPIc9Z7+w+H9ZD6uI2+lfjuMd1ttjUtFabJGd+VnsyGrXGp6JULzmAoqF3e8BwG54ZEKQctVwgIAKoSxFk+6DnwFoKezUtR13cDmCyVawdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('05923d5e280fe26a3001f8546ca8fd77')


@app.route("/callback", methods=['POST']) # line server把訊息轉載到"自訂網址", 進而觸發下方程式碼
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "很抱歉，我不知道您說什麼"

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message( # 主要回覆功能為此段
            event.reply_token,
            sticker_message)

        return

    if msg in ['hi', 'Hi']: # 用in搭配清單傳出True/False, 來納入不同書寫格式
        r = '嗨！'
    elif msg == '你吃飯了嗎':
        r = '還沒誒'
    elif msg == '你今年幾歲':
        r = '這是秘密'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎？'

    line_bot_api.reply_message( # 主要回覆功能為此段
                event.reply_token,
                TextSendMessage(text=r))

if __name__ == "__main__":
    app.run()