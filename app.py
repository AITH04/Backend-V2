import os

import userstatemanager
import dialogsys
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
    print(f'::Dialog SYS::\n有人拜訪首頁\n==========================================')
    return "這是對話引擎\nINPUT FORMAT: {request_source:Line, userId:2020081000011,	action:TextMsg, msg:有}"


# 對話引擎
@app.route('/api', methods=['POST'])
def dialog():
    try:
        source = 'linebot' #紀錄資料來源
        userId  = request.json["userId"] # 使用者ID: 用於讀取json檔內容
        message = request.json["msg"] # 使用者輸入的文字訊息
        print("::Dialog SYS:: 資料讀取成功")
    except Exception as e:
        print(f'::SYS錯誤訊息::\n{e}\n==========================================')
        return jsonify({"except": '\n\n'+e})
    return jsonify(dialogsys.main(source, userId, message))


# heroku專用，偵測heroku給我們的port
if __name__=="__main__":
    #app.run(host='0.0.0.0', port=os.environ['PORT']) # 執行於Heroku主機
    #app.run(host="0.0.0.0",port=5001) # 執行於本地端
    app.run() # 基本款