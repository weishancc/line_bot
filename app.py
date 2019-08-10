from flask import Flask, request, abort

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

line_bot_api = LineBotApi('wW36xH4YWdBT7PATVU2jqdqTM1IQVpBWUxt37yCnuMKkZv46PdRYErmEDQZrbCoSk92Sau9GPVgiUUU6YGVLC0/OJd2XT/1/ckfVui6LGrc2WrQ42By4WdvDMcj2QOU/I3B9PC3FMITEw68Ts3eVWQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1a74c11755a2f1d05fa9f2efe9de7459')


@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理訊息
#import jieba.posseg as pseg

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #ques = event.message.text
    #cuts = pseg.lcut(ques)
    #back = ""
    #for cut in cuts:
        #if(cut.flag =='n'):
            #back = cut.word
    back='message'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=back))

if __name__ == "__main__":
    app.run()
