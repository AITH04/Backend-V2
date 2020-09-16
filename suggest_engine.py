import requests
# 引用生成詞
# import thanks_word.generate_words as callAPIThxword
from thanks_word import generate_words as callAPIThxword
# 引用產品服務A
# import connect2postgres.get_tag_from_productid as callAPITags
from connect2postgres import get_tag_from_productid as callAPITags
# 引用產品服務B
# import E.get_product_info as callAPIProductInfo
from E import  get_product_info as callAPIProductInfo


# 假設變數區 ==================
state_list = ['wait_user', 'ask_interest', 'first_question', 'question_loop_False', 'question_loop_True', 'end_conversation']
# API 連線元件 ================
# def callAPITags(json_input={"conds": ["牛仔","男裝"]}):
#     '''
#     # 呼叫產品服務A
#     :param json_input:
#     :return:
#     '''
#     # 從.txt 讀取API網址
#     with open('tagApiURL.txt', 'r', encoding='utf8') as f:
#         apiURL = f.read()
#     # 呼叫API網址取得回應，儲存於response
#     response = requests.post(apiURL, json=json_input)
#     print("::SYS訊息:: 成功呼叫產品服務A API")
#     response = response.json()
#     print('return content: ', response)
#     print('return object type: ', type(response))
#     return response
#
#
# def callAPIProductInfo(json_input={"conds": ["牛仔","男裝"]}):
#     '''
#     呼叫產品服務B
#     :param json_input:
#     :return:
#     '''
#     # 從.txt 讀取API網址
#     with open('productBApiURL.txt', 'r', encoding='utf8') as f:
#         apiURL = f.read()
#     # 呼叫API網址取得回應，儲存於response
#     response = requests.post(apiURL, json=json_input)
#     print("::SYS訊息:: 成功呼叫產品服務B API")
#     response = response.json()
#     print('retrun content: ', response)
#     print('return object type: ', type(response))
#     return response
#
#
# def callAPIThxword(json_input={"subject": "NAME0", "conds": ["牛仔","男裝"]}):
#     '''
#     呼叫文本產生器
#     :param json_input:
#     :return:
#     '''
#     # 從.txt 讀取API網址
#     with open('thxApiURL.txt', 'r', encoding='utf8') as f:
#         apiURL = f.read()
#     # 呼叫API網址取得回應，儲存於response
#     response = requests.post(apiURL, json=json_input)
#     print("::SYS訊息:: 成功呼叫文本產生器 API")
#     response = response.json()
#     print('retrun content: ', response)
#     print('return object type: ', type(response))
#     return response


# 各場景實作細節=========================================
def state6to1(json_object):
    print('::推薦系統訊息:: in test.... state6to1 - start')
    # 更新現在狀態
    json_object['json']['cur_state'] = 'wait_user'
    print('::推薦系統訊息:: in test.... state6to1 - finish')
    return json_object['json']


def state1to2(json_object):
    print('::推薦系統訊息:: in test.... state1to2 - start')
    # 讀取需要的input: 使用者輸入了贈禮對象
    user_input = json_object['outside']['msg']
    # 更新贈禮對象
    json_object['json']['subject'] = user_input
    # 更新現在狀態
    json_object['json']['cur_state'] = 'ask_interest'
    print('::推薦系統訊息:: in test.... state1to2 - finish')
    return json_object['json']


def state2to3(json_object):
    print('::推薦系統訊息:: in test.... state2to3 - start')
    # 讀取需要的input: 使用者輸入了興趣類別
    user_input = json_object['outside']['msg']
    # 更新贈禮對象
    json_object['json']['interested_things'] = user_input
    #    tags = {'conds': json_object['json']['conds']}
    # 呼叫產品服務A
    response = callAPITags(json_object['json']['conds'])
    # 更新下一個TAG
    json_object['json']['next_tag'] = response['next_tag']
    # 更新產品數量
    json_object['json']['product_cnt'] = response['product_cnt']
    # 更新現在狀態
    json_object['json']['cur_state'] = 'first_question'
    print('::推薦系統訊息:: in test.... state2to3 - finish')
    return json_object['json']


def state3(json_object):
    '''
    回報送禮對象、候選禮物數。轉場進入詢問loop，詢問對Ntag是否有興趣
    :param json_object:
    :return:
    '''
    print('::推薦系統訊息:: in test.... state3 - start')
    # 讀取需要的input: 使用者感興趣的tags
    #tags = {'conds': json_object['json']['conds']}
    response = callAPITags(json_object['json']['conds'])
    print("收到產品服務A回傳值:",str(response))
    json_object['json']['next_tag'] = response['next_tag']
    json_object['json']['product_cnt'] = response['product_cnt']
    json_object['json']['cur_state'] = 'first_question'
    print('::推薦系統訊息:: in test.... state3 - finish')
    return json_object['json']


def state3to4(json_object):
    print('::推薦系統訊息:: in test.... state3to4 - start')
    # 重新拿一個Ntag
    # tags = json_object['json']['conds']
    # tags = {'conds': tags}
    response = callAPITags(json_object['json']['conds'])
    json_object['json']['next_tag'] = response['next_tag']
    json_object['json']['cur_state'] = 'question_loop_False'
    print(f"load result:\n\t tags: {json_object['json']['conds']}\n\t Ntag = {json_object['json']['next_tag']}")
    print('::推薦系統訊息:: in test.... state3to4 - finish')
    return json_object['json']


def state3to5(json_object):
    '''
    已確認使用者對Ntag有興趣，把Ntag收進conds，檢查後選禮物數量確定下一步去哪
    :param json_object:
    :return:
    '''
    threshold = 10
    print('::推薦系統訊息:: in test.... state3to5 - start')
    # 讀取需要參數: tags,Ntag
    tags = json_object['json']['conds']
    Ntag = json_object['json']['next_tag']
    tags.append(Ntag)
    #tags = {'conds': tags}
    print(f'load result:\n\t tags: {tags}\n\t Ntag = {Ntag}')
    # 透過API要資料，並更新對應值
    response = callAPITags(tags)
    json_object['json']['next_tag'], json_object['json']['product_cnt'] = response['next_tag'], response['product_cnt']
    # 依據候選禮物數判斷下一步
    if response['product_cnt'] <= threshold:
        # 進入場景6
        new_json_object = state3to6(json_object)
        #json_object['json']['cur_state'] = 'end_conversation'
        return new_json_object
    else:
        # 轉換到場景5
        json_object['json']['cur_state'] = 'question_loop_True'
        print('::推薦系統訊息:: in test.... state3to5 - finish')
        return json_object['json']


def state3to6(json_object):
    '''
    透過API拿商品資訊(品名、連結)& 感謝詞
    :param json_object:
    :return:
    '''
    print('::推薦系統訊息:: in test.... state3to6 - start')

    # 透過API拿產品資訊，並更新對應值
    #   讀取需要參數: tags, subject
    tags = {'conds': json_object['json']['conds']}
    print(f'load result:\n\t tags: {tags}')
    #   解析回傳json並更新對應值
    response = callAPIProductInfo(json_object['json']['conds'])
    json_object['json']['products'] = response
    print(f'測試行1: {json_object}')

    # -----------------------------
    # 透過API拿感謝詞，並更新對應值
    #   讀取需要參數:  subject, tags
    response = callAPIThxword(json_object['json']['subject'], json_object['json']['conds'])
    json_object['json']['thx words'] = response['thx words']

    # -----------------------------
    # 狀態轉換
    json_object['json']['cur_state'] = 'end_conversation'
    print(f"check result:\n\t product: {json_object['json']['products']}\n\t thx word: {json_object['json']['thx words']}")
    print('::推薦系統訊息:: in test.... state3to6 - finish')
    return json_object['json']


# 兩個路線分配器 =================================
def decisionmix(json_object):
    print('decisionmix')
    # 讀取需要的input: 使用者表示了有興趣或沒興趣
    user_input = json_object['outside']['msg']
    if user_input == '有':
        # 進入場景5
        #json_object['json']['cur_state'] = 'question_loop_True'
        new_json_object = state3to5(json_object)
        return new_json_object
    elif user_input == '無':
        # 進入場景4
        new_json_object = state3to4(json_object)
        #json_object['json']['cur_state'] = 'question_loop_False'
        return new_json_object
    else:
        print('error input in decisionMIX')


# 主程式，系統會先跑這支函式 ========================
def main(userdata):
    # 先整理對話引擎傳來的 使用者資料&前端訊息
    try:
        # 使用者資料
        user_msg  = userdata["json"]
        print(" 讀取JSON")
        # 前端訊息
        front_input  = userdata["outside"]
        print(" 讀取OUTSIDE")
        # 裝後面要用的參數
        json_object = {"json":user_msg, "outside":front_input}
    except Exception as e:
        print(f'::SYS錯誤訊息::\n{e}\n==對話系統傳來資料不符================================')
        return '\n\n', e
    print(f"::SYS訊息:: 輸入參數 {json_object}")

    # 根據現在的狀態(cur_state)進入function
    cur_state = json_object['json']['cur_state']
    if cur_state == 'end_conversation':
        json_return = state6to1(json_object)
    elif cur_state == 'wait_user':
        json_return = state1to2(json_object)
    elif cur_state == 'ask_interest':
        json_return = state2to3(json_object)
    elif cur_state == 'first_question':
        json_return = decisionmix(json_object)
    #elif cur_state == 'question_loop_False':
    #    json_return = state5(json_object)
    #elif cur_state == 'question_loop_True':
    #    json_return = state6(json_object)
    else:
        json_return = 'ERROR! in 推薦系統MAIN'
    print(json_return)
    return json_return


# 測試區域 =======================================
test_json = {
            "json":{
                "userId": 'test0000',
                "cur_state": state_list[1],
                "subject": '媽媽',
                "interested_things": None,
                "conds": ['男裝','節帶'],
                "next_tag": '123',
                "product_cnt": -1
                        },
            "outside":{
                "action": '',
                "msg": '男裝'
                }}
if __name__ == "__main__":
    main(test_json)

# 測試區域結束 ====================================
