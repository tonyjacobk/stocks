from flask import Flask, render_template
from aiven import get_rows,get_broker,get_stock,get_stock_partial
import urllib.parse
app = Flask(__name__)
rows_per_page=20
# MySQL configurations
@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    data,total_pages=get_rows(page,20)
    return render_template('index.html', data=data, page=page, total_pages=total_pages)
@app.route('/brk/<brok>')
@app.route('/brk/<brok>/<int:page>')
def search_broker(brok,page=1):
    brok=urllib.parse.unquote(urllib.parse.unquote(brok))
    print(brok)
    data,total_pages=get_broker(page,rows_per_page,brok)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,broker=brok)
@app.route('/stok/<stock>')
@app.route('/stok/<stock>/<int:page>')
def search_stock(stock,page=1):
    print (stock)
    stock=urllib.parse.unquote(urllib.parse.unquote(stock))
    print(stock)
    data,total_pages=get_stock(page,rows_per_page,stock)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,company=stock)

@app.route('/partialstok/<stock>')
@app.route('/partialstok/<stock>/<int:page>')
def search_stock_partial(stock,page=1):
    print (stock)
    stock=urllib.parse.unquote(urllib.parse.unquote(stock))
    print(stock)
    data,total_pages=get_stock_partial(page,rows_per_page,stock)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,company=stock)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


