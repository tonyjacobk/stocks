from flask import Flask, render_template,Blueprint
from aiven import get_rows,get_broker,get_stock,get_stock_partial
from price import get_price,load_price,get_date
from download_bhav_copy  import bhav_main
rows_per_page=20

report_bap=Blueprint("report",__name__)

# MySQL configurations
@report_bap.route('/')
def test():
    rows,res=load_price()
    report_date=get_date(rows
    print ("Will this print")
    return("Will this print")







