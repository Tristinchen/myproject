
import requests
import json
import time
import simplejson as simplejson
import pymysql
from pymysql.converters import escape_string
import getNewToken



def getToken():
    db = pymysql.connect(host='localhost', port=3306, user='root', database='core', charset='utf8', autocommit=True)
    cur = db.cursor()
    tokenSQL = "select * from token where store_name='maden'"
    cur.execute(tokenSQL)
    result=cur.fetchall()
    expiretime=result[0][2]
    token=result[0][1]
    nowTime=int(time.time())
    if int(expiretime)+560 >= nowTime:
        print("token 还在")
        newToken=token

    else:
        print("token 失效了")
        newToken=getNewToken.get_refreshToken()
        #newToken='eyjhbgcioijiuzuxmij9.eyJhcHBLZXkiOiJmYThiODYyYzRjNDEwN2VhOWRlNzk3ZjA3NGNmMGMwYzcxOTJmOWM2Iiwic2VsbGVySWQiOiIyMDAxMTI2MDI1Iiwic3RvcmVJZCI6IjE2NTQ5MjgxMzg1MjQiLCJ2ZXJzaW9uIjoiVjIiLCJkb21haW4iOiJ'
        tokenUpdateSQL="update token SET token='%s',expiretime=%s where store_name='maden'" % (newToken,nowTime)
        print (tokenUpdateSQL)
        cur.execute(tokenUpdateSQL)
    cur.close()
    db.close()

    return newToken

reFreshToken='Bearer '+str(getToken())

print(reFreshToken)

def updateProducts(products_infos):

    db = pymysql.connect(host='localhost', port=3306, user='root', database='core', charset='utf8', autocommit=True)
    cur = db.cursor()
    table = 'products'

    update_num=0
    insert_num=0

    for item in products_infos:
        #print("=============================================================================================================")
        #print(item)
        #print("=============================================================================================================")
        product_name=item['title']
        product_id=item['id']

        if 'image' in item.keys():
            images=item['image']
            if images is None:
                image = ''
            else:
                image = item['image']['src']
        else:
            image = ''
        # try:
        #     image = item['image']['src']
        # except:
        #     print("商品数据缺失")
        #     image = ''
        create_time = int(time.mktime(time.strptime(item['created_at'],'%Y-%m-%dT%H:%M:%S%z')))
        status=item['status']
        variants=item['variants']
        for i in range(len(variants)):
            sku_id = variants[i]['id']

            sku_code=variants[i]['sku'].replace("{","").replace("}","")


            sku_option = variants[i]['title']
            price = variants[i]['price']
            sale_price = variants[i]['compare_at_price']
            inventory_item_id = variants[i]['inventory_item_id']
            inventory = variants[i]['inventory_quantity']
            select_sql = "select sku_id from %s where sku_id='%s'" % (table, sku_id)
            cur.execute(select_sql)
            if cur.fetchone():
                # print(update_sql)
                sql2 = "update %s set raw_data='{json2}', image='{imagejson2}', status='%s',sku_code='%s',price='%s',sale_price='%s',inventory='%s' where sku_id=%s " % (
                    table, status, sku_code,price,sale_price,inventory, sku_id)

                update_sql = sql2.format(json2=escape_string(simplejson.dumps(item)),
                                         imagejson2=escape_string(simplejson.dumps(image)))
                cur.execute(update_sql)

                update_num += 1
            else:
                sql1 = "insert into %s (product_id,product_name,image,create_time,status,sku_id,sku_code,sku_option,price,sale_price,inventory_item_id,inventory,raw_data) " \
                       "values ('%s','%s','{imagejson}','%s','%s','%s','%s','%s','%s','%s','%s','%s','{json}') " \
                       % (table, product_id, product_name, create_time, status, sku_id, sku_code, sku_option, price,
                          sale_price, inventory_item_id, inventory)
                #print(sql1)
                insert_sql = sql1.format(json=escape_string(simplejson.dumps(item)),
                                         imagejson=escape_string(simplejson.dumps(image)))
                cur.execute(insert_sql)
                insert_num += 1



        #product_id=variants[0].get("product_id")

        #print(product_name)
        #print(product_id)


    cur.close()
    db.close()
    l=[update_num,insert_num]
    return l


def get_AllProducts(reFreshToken):
    url = "https://maden.myshopline.com/admin/openapi/v20220901/products/products.json"

    payload={}
    Firstheaders = {
        # 'limit': '100', # 一次最多1000个,默认50
        'Authorization': reFreshToken,
        # 'since_id': '0',
        #'page_info': 'eyJzaW5jZUlkIjoiMTYwNTQ0NTk1MDE0MTc5NzE0MDUyNDIxMzYiLCJkaXJlY3Rpb24iOiJuZXh0In0',
        #'rel':'next'
    }
    totalupdatenum=0
    totalinsertnum=0

    while True:
    #print(headers)
        response = requests.request("GET", url, headers=Firstheaders, data=payload)
        products_infos=json.loads(response.text).get("products")
        l=updateProducts(products_infos)
        totalupdatenum += l[0]
        totalinsertnum += l[1]
        link = response.headers.get("link")
        print(link)
        if "next" in link:
            url = link.split(';', 1)[0][1:-1]
            print(url)
        else:
            break
        #print(products_infos)
        #print("以下是获取的商品数据：", products_infos)
        print("累计更新%s,累计插入%s"%(totalupdatenum,totalinsertnum))

    print(totalupdatenum,totalinsertnum)

get_AllProducts(reFreshToken)

print("更新完啦")







