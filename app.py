import os
import subprocess
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextMessage

app = Flask(__name__)
# yolo-venv\Scripts\activate.bat
# ใส่ Channel Access Token และ Channel Secret ของคุณที่นี่

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)

    # กำหนดชื่อไฟล์ที่จะบันทึกภาพ
    filename = f"images/image_{event.message.id}.jpg"


    with open(filename, 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # ส่งข้อความยืนยันกลับไปยังผู้ส่ง
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"บันทึกภาพแล้ว: {filename}")
    )

    # เรียก detect.py โดยใช้ subprocess.run()
    #detect_command = f"python detect.py --source images/image_{event.message.id}.jpg"
    #subprocess.run(detect_command, shell=True)

if __name__ == "__main__":
    app.run()
