#-*- coding: utf-8 -*-

from flask import Flask,render_template
from getProduct import getProducts

app = Flask(__name__)

data=getProducts()
print(data)
@app.route('/')
def hello_world():
   return render_template('index.html',data=data)


if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')