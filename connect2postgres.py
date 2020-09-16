import psycopg2
from random import randint


def get_tag_from_productid(tag_name_list=["男裝", "牛仔"]):
    # 連接資料庫並抓取

    # 連線帳密要改過
    conn = psycopg2.connect(database="gift_expert_testenv", user="gift_backend", password="master",
                            host="172.104.89.11", port="5432")
    cur = conn.cursor()
    if len(tag_name_list) > 1:
        print(f"兩個以上搜尋條件,條件為: {tag_name_list}")
        # tag_name_list == ['休閒', '亮眼']
        tag_name_list_str = "'" + "','".join(tag_name_list) + "'"
        # tag_name_list_str == '休閒','亮眼'
        sql_query = "select tag_name, product_id from product_ptags where product_ptags.tag_name in (" + tag_name_list_str + ");"
    elif len(tag_name_list) == 1:
        print(f"只有一個搜尋條件,條件為: {tag_name_list}")
        tag_name_list_str = "'" + tag_name_list[0] + "'"
        sql_query = "select tag_name, product_id from product_ptags where product_ptags.tag_name in (" + tag_name_list_str + ");"
    elif len(tag_name_list) == 0:
        sql_query = "SELECT tag_name, product_id from product_ptags;"
    print(f"SQL指令: {sql_query}")
    # where product_ptags.tag_name in ('休閒','亮眼');
    cur.execute(sql_query)

    rows = cur.fetchall()
    # rows == [("tagname", productid), ()....]
    pid_dic = {}
    final_pid_list = []
    for row in rows:
        # row == ("tagname", productid) row[1]==productid
        # sample:    row == ("123", 18)
        if (row[1] in pid_dic.keys()):
            pid_dic[row[1]] += 1
            # pid_dic == {18: 2}
            if pid_dic[row[1]] == len(tag_name_list):
                final_pid_list.append(str(row[1]))
        else:
            # pid_dict == {}
            pid_dic[row[1]] = 1
            # pid_dic == {18: 1}
            if len(tag_name_list) == 1:
                final_pid_list.append(str(row[1]))

    # 以上為選出符合條件的productid

    # 處理輸入為空字串的情形 aka連一個標籤都沒有
    if len(tag_name_list) == 0:
        tag_dic = {}
        for row in rows:
            if (row[0] in tag_dic.keys()):
                # 把商品編號對應的值 +1
                tag_dic[row[0]] += 1
            # 商品編號 不曾 出現在新表
            else:
                # pid_dict == {}
                # 用商品編號在pid_dic裡新增 key=商品編號 value=1的pair
                tag_dic[row[0]] = 1
        valid_tag = []
        for key in tag_dic.keys():
            if tag_dic[key] > 300:
                valid_tag.append(key)
        index = randint(0, len(valid_tag) - 1)
        product_cnt = len(pid_dic)
        conn.close()
        return {
            "next_tag": valid_tag[index],
            "product_cnt": product_cnt
        }
    # final_pid_list == ['18', '27']
    pid_string = ",".join(final_pid_list)
    # pid_string = "18,27"
    product_cnt = len(final_pid_list)

    #

    second_sql_query = "select tag_name from product_ptags where product_ptags.product_id in (" + pid_string + ") order by random() limit 1;"
    print(f"SQL指令: {second_sql_query}")

    # select tag_name from product_ptags where product_ptags.product_id in (18,27) order by random() limit 1;"
    cur.execute(second_sql_query)

    random_new_tag = cur.fetchall()
    # random_new_tag == [['sample']]
    conn.commit()
    conn.close()

    return {
            "next_tag": random_new_tag[0][0],
            "product_cnt": product_cnt
            }