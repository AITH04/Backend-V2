import userstatemanager
import requests
from suggest_engine import main as callAPIKernal

# def callAPIKernal(json_input):
#     '''
#     # 呼叫推薦服務
#     :param json_input:
#     :return:
#     '''
#     with open('apiURL.txt', 'r', encoding='utf8') as f:
#         url = f.read()
#     print('\n::Dialog SYS:: callAPIKernal postinput \n', json_input)
#     print('::Dialog SYS:: postinput type: \n', type(json_input))
#     response = requests.post(url, json=json_input)
#     response = response.json()
#     print('\n::Dialog SYS:: retrun content \n', response)
#     print('::Dialog SYS:: return object type: \n', type(response))
#     return response


def returnByState(userstate):
    # 晚點再建 我累了想休息
    pass


def main(source, userId, message):
    # 讀取使用者資料
    user_state = userstatemanager.GetUserStae(source, userId)
    print(f'\nload user state:\n{user_state}')
    # 組合成API input
    api_input = {"json": user_state, "outside": {"action": "","msg": message}}
    print('\n::Dialog SYS::\nAPI input: ', api_input)
    print('\n::Dialog SYS:: data type: ', type(api_input))

    # 呼叫 推薦引擎
    print('::Dialog SYS:: dialogsys.main呼叫kernal')
    response = callAPIKernal(api_input)
    print('::Dialog SYS:: 順利取得kernal API回覆= ',str(response) )
    user_state = response
    print('\n::Dialog SYS::\nuser_state: ', user_state)
    print('\n::Dialog SYS:: data type : ', type(user_state))
    # 保存使用者資料
    print(userstatemanager.UpdateUserState(source, user_state['userId'], user_state['cur_state'], user_state['subject'], user_state['interested_things'], user_state['conds'], user_state['next_tag'],
                                           user_state['product_cnt']))
    # 依據場景設定回傳值對方
    # 先pass
    return user_state


if __name__ == "__main__":
    main('linebot','test000','Hi')