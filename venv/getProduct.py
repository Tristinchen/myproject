import pymysql
import json

def getProducts():
   db = pymysql.connect(host='119.8.117.235', port=3306, user='root', password='Sy123456.', database='core', charset='utf8', autocommit=True,cursorclass=pymysql.cursors.DictCursor)
   cur = db.cursor()
   table = 'product_1688source'
   sql1 = "select distinct product_id from %s limit 10" % table
   cur.execute(sql1)
   allproducts = cur.fetchall()
   # print(allproducts)
   all_info=[]
   for product in allproducts:
      id=product["product_id"]
      # print(id)
      sql2="select product_code,product_title,product_img,price,sale_price,source_url from %s where product_id='%s' limit 1" %(table,id)
      cur.execute(sql2)
      product_info = cur.fetchall()
      # print("product_info:", product_info)
      sql_color="select distinct v_color from %s where product_id=%s" %(table,id)
      cur.execute(sql_color)
      product_color = cur.fetchall()
      # print(product_color)
      sku_info=[]
      for colors in product_color:
         color=colors["v_color"]
         sql_skuinfo="select v_color,moreinfo,sku_code,inventory1688 from %s where product_id='%s' and v_color='%s'" %(table,id,color)
         cur.execute(sql_skuinfo)
         skuinfo = cur.fetchall()
         # print(skuinfo)
         sku_info.extend(skuinfo)
      # print(sku_info)
      all_info.extend(product_info)
      all_info[len(all_info)-1]["sku_infos"]=sku_info
      # print("all_info:",all_info)
   all_info2=json.dumps(all_info)

   return all_info2

