import psycopg2
import os
import json

# 這是產品服務B的程式碼

#app = Flask(__name__)
#app.config['JSON_AS_ASCII'] = False #make json show in Chinese


# with open('IDPW.json','r',encoding='utf8') as f:
#    jsonfile = f.read()
#    jsonfile = json.loads(jsonfile)

# @app.route("/")
# def hello():
#     print('::有人拜訪首頁::')
#     return "I'm product service B"
#
# @app.route('/api', methods=['GET','POST'])
# # @app.route('/productserviceB', methods=['POST'])
# def request_for_product():
#     input = request.json['conds']
#     # input = ['休閒', '百搭']
#     return jsonify(get_product_info(input))


def get_product_info(tag_name_list = ['休閒', '百搭']):

    # 這邊可以改成以txt保存密碼的方式
    conn = psycopg2.connect(database="gift_expert_testenv", user="gift_backend", password="master",
                            host="172.104.89.11", port="5432")
    cur = conn.cursor()

    tag_name_list_str = "'" + "','".join(tag_name_list) + "'"
    sql_query = "select product_id from product_ptags where product_ptags.tag_name in (" + tag_name_list_str + ");"
    cur.execute(sql_query)

    rows = cur.fetchall()  # rows == [product_id]
    row_lst = []
    for row in rows:
        row_lst.append(row[0])
    final_pid_list = list(set(rows))  # 得出product_id的lst
    row_lst = []
    for row in final_pid_list:
        row_lst.append(row[0])
    row_lst.sort()
    pid_string = ""
    for row in row_lst:
        pid_string += ("'" + str(row) + "',")
    pid_string = pid_string[:-1]
    second_sql_query = "select page_id, description from products where products.id in (" + pid_string + ") limit 10;"
    # second_sql_query = "select page_id, description from products where products.id in (" + pid_string + ");"
    cur.execute(second_sql_query)
    rows = cur.fetchall()
    id_lst = []
    description_lst = []

    for row in rows:
        id_lst.append(row[0])  # 得出id lst  #此id 是page_id
        tmp = list(row[1])
        product_name = []
        for ch in tmp:
            if ch != "|":
                product_name.append(ch)
            else:
                # description_lst.append("".join(product_name).replace(" ", "")) #去空白
                description_lst.append("".join(product_name))
                break

    pages_id_str = ""
    for ele in id_lst:
        pages_id_str += "'" + str(ele) + "',"
    pages_id_str = pages_id_str[:-1]
    third_sql_query = "select url from pages where pages.id in (" + pages_id_str + ");"
    cur.execute(third_sql_query)
    rows = cur.fetchall()  # 第三道 取商品網址的 SQL命令
    url_lst = []
    for row in rows:
        url_lst.append(row[0])
    products_dict = {}  # 最終要回傳的空字典
    for i in range(0, len(id_lst)):
        # print(description_lst[i], url_lst[i])
        products_dict[description_lst[i]] = url_lst[i]

    conn.commit()
    conn.close()
    return products_dict


# if __name__ == "__main__":
#     #app.run(host='0.0.0.0', port=os.environ['PORT'])
#     app.run()