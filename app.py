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
from dbmdl import *

#app = Flask(__name__)

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

#分辨物品種類（switch）
def cate(x):
    return {
        'bn':'背景',
        'fn':'旗幟',
        'wn':'偽裝階級',
        'jn':'階級效果',
        'pn':'櫥窗道具',
        'en':'櫥窗效果',
        'cn':'角色效果',
        'ban':'水球'
    }.get(x,'category')

# 處理訊息
import jieba.posseg as pseg
import jieba

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #新增自定義詞庫
    jieba.load_userdict('./dict.txt')

    ques = str(event.message.text)
    cuts = pseg.lcut(ques)
    find = False    #找到名詞（物品）
    lst = ['bn','wn','jn','fn', 'pn','en','cn','ban']   #物品種類（詞性）

    #cut.word:物品名稱 ; cut.flag:詞性
    for cut in cuts:
        if(cut.flag in lst):
            find = True

            #搜尋資料
            datas = ItemInfo.query.filter_by(name = cut.word).first()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = ('物品名稱： ' + cut.word + '\n價格： ' + str(datas.price) + '\n庫存： ' + str(datas.stock) + '\n種類： ' + cate(datas.category))))

    if(not find):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = '請提問物品（完整名稱）,我才看得懂啦 \n若是已打完整名稱未找到,那就是我沒放進資料庫裡啦(QAQ)'))


if __name__ == "__main__":
    app.run()
