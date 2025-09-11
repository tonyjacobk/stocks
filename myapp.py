from flask import Flask, render_template,Blueprint
from aiven import get_rows,get_broker,get_stock,get_stock_partial
from price import get_price,load_price,get_date
from download_bhav_copy  import bhav_main
import urllib.parse
rows_per_page=20
rows,res=load_price()
report_date=get_date(rows)
report_bp=Blueprint("report",__name__)

# MySQL configurations
@report_bp.route('/')
@report_bp.route('/<int:page>')
def index(page=1):
    print(res)
    print(rows)
    data,total_pages=get_rows(page,20)
    get_price(data,rows)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,report_date=report_date)
@report_bp.route('/brk/<brok>')
@report_bp.route('/brk/<brok>/<int:page>')
def search_broker(brok,page=1):
    brok=urllib.parse.unquote(urllib.parse.unquote(brok))
    print(brok)
    data,total_pages=get_broker(page,rows_per_page,brok)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,broker=brok,report_date=report_date)
@report_bp.route('/stok/<stock>')
@report_bp.route('/stok/<stock>/<int:page>')
def search_stock(stock,page=1):
    print (stock)
    stock=urllib.parse.unquote(urllib.parse.unquote(stock))
    print(stock)
    data,total_pages=get_stock(page,rows_per_page,stock)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,company=stock,report_date=report_date)

@report_bp.route('/partialstok/<stock>')
@report_bp.route('/partialstok/<stock>/<int:page>')
def search_stock_partial(stock,page=1):
    print (stock)
    stock=urllib.parse.unquote(urllib.parse.unquote(stock))
    print(stock)
    data,total_pages=get_stock_partial(page,rows_per_page,stock)
    return render_template('index.html', data=data, page=page, total_pages=total_pages,company=stock,report_date=report_date)






