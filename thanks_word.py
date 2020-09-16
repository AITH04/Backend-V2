import random
# 這是生成感謝詞的程式碼


def generate_words(NAME0 = '秉鴻', TAGS_list = ['小美', '佑軒']):
    if len(TAGS_list)>3:
        random.shuffle(TAGS_list)
        TAGS_3 = TAGS_list[:3]
        TAGS = '、'.join(TAGS_3)
    else:
        random.shuffle(TAGS_list)
        TAGS = '、'.join(TAGS_list)
    thx_words = '感謝詞（可以用在卡片上）\n===\n 親愛的'+ NAME0 + '\n\n幸福的生活中少不了你的陪伴。\n\n我知道你喜歡'+TAGS+'，所以特地挑選了這個禮物，希望你會喜歡。'
    return {'thx words':thx_words}



