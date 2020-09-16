import json
import os


# version 1.0
# developer 674
# perpose as backen of app.py, support app.py to maintain its userstate record whitch is stored as json format in .json


def SetInitialValue(userId):
    '''
    回傳使用者資料的初始值
    :input userId: str-使用者id
    :return: dict-使用者資料初始值
    '''
    return_obj = {}
    return_obj['userId']    = userId # 使用者id，比對用
    return_obj['cur_state'] = 'end_conversation' # 現在狀態
    return_obj['subject']   = "None" # 送禮對象
    return_obj['interested_things'] = "None" # 興趣類別
    return_obj['conds']     = [] # 感興趣的標籤
    return_obj['next_tag']  = "None" # 待詢問標籤
    return_obj['product_cnt']       = -1 # 待選禮物數，設定-1為初始值
    return return_obj


def GetUserStae(request_source, userid):
    '''
    讀取使用者資料JSON檔，並回傳
    :input request_source: str 訊息來源LineBot或者Web
    :input userid: str 使用者ID
    :return: 使用者狀態(json)
    '''
    # 兩種檔案名稱，以使用者來源區分
    #       * lineuserstate_<由line傳來的userid>.json
    #       * webuserstate_<由web傳來的userid>.json
    # 收到request，請求回傳使用者資料
    # 產生檔案路徑
    if request_source == 'linebot':
        file_name = 'LINEuserstate_' + userid + '.json'
    elif request_source == 'web':
        file_name = 'WEBuserstate_' + userid + '.json'
    else:
        print(f'wrong source: {request_source}')
    print('filename:',file_name)
    file_path = os.path.join(os.getcwd(), 'userstate', file_name)
    print('filepath:',file_path)
    # 搜尋檔案 →找到，讀取
    if os.path.exists(file_path) == True:
        with open(file_path, 'r', encoding='utf8') as json_file:
            content = json.load(json_file)
        print(f'==================\n{content}\n=====================')
        print(f'user[{userid}] personal data loads SUCCESS')
    # 搜尋檔案 →找不到，新建，給初始值
    else:
        print('the file is not exist, so I create a new one ')
        with open(file_path, 'w', encoding='utf8') as json_file:
            content = SetInitialValue(userid)
            json.dump(content, json_file, indent=4, ensure_ascii=False)
        print(f'write in content :\n{content}\n')
        print(f'new user [{userid}] personal data creates SUCCESS')
    # 回傳response
    print('\n::return_content:',content)
    print('::return_datatype:', type(content))
    return content


def UpdateUserState(request_source, userid, cur_state, subject, interested_things, conds, next_tag, product_cnt):
    '''
    更新使用者狀態JSON檔
    :param request_source: str-訊息來源LineBot或者Web
    :param userid: str-使用者ID
    :param cur_state: str-使用者現在狀態
    :param subject: str-送禮對象
    :param interested_things: str-興趣類別
    :param conds: list-感興趣標籤
    :param next_tag: str-待詢問標籤
    :param product_cnt: int-候選禮物數
    :return: True: 保存成功
             False: 保存失敗
    '''
    # 收到request，請求回傳更新使用者資料
    # 解析request傳來的json內容[暫時沒有]
    #userid = '2020081500000000'
    #example = request.json['conds']
    #cur_state = None
    #subject   = None
    #interested_things = None
    #conds = None
    #next_tag = None
    #product_cnt = 25
    # 檢查cur_state格式
    state_list = [None, 'wait_user', 'ask_interest', 'first_question', 'question_loop_False', 'question_loop_True', 'end_conversation']
    if (cur_state in state_list) == False:
        print('Invalid Value in cur_state: check your format and send request again')
        return False,'Invalid Format in cur_state'

    # 產生檔案路徑
    if request_source == 'linebot':
        file_name = 'LINEuserstate_' + userid + '.json'
    elif request_source == 'web':
        file_name = 'WEBuserstate_' + userid + '.json'
    else:
        print(f'wrong source: {request_source}')
    print('filename:', file_name)
    file_path = os.path.join(os.getcwd(), 'userstate',file_name)
    print('filepath:', file_path)

    #所有已知訊息整理成json格式
    save_obj = {}
    save_obj['userId'] = userid  # 使用者id，比對用
    # 處理傳4存3、傳5存3
    if cur_state == "question_loop_False" or cur_state == "question_loop_True":
        cur_state = "first_question"
    elif cur_state == "end_conversation":
        with open(file_path, 'w', encoding='utf8') as json_file:
            content = SetInitialValue(userid)
            json.dump(content, json_file, indent=4, ensure_ascii=False)
        return True, 'saves SUCCESS'
    save_obj['cur_state'] = cur_state  # 現在狀態
    save_obj['subject'] = subject  # 送禮對象
    save_obj['interested_things'] = interested_things  # 興趣類別
    save_obj['conds'] = conds  # 感興趣的標籤
    save_obj['next_tag'] = next_tag  # 待詢問標籤
    save_obj['product_cnt'] = product_cnt  # 待選禮物數，設定-1為初始值

    # 存入JSON檔中
    with open(file_path, 'w', encoding='utf8') as json_file:
        json.dump(save_obj, json_file, indent=4, ensure_ascii=False)
    print(f'write in content :\n{save_obj}\n')
    print(f'user [{userid}] personal data saves SUCCESS')
    return True, 'saves SUCCESS'

# 定期清理webuser的json
# 待開發