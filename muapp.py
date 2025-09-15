from flask import Flask, render_template,Blueprint
report_bap=Blueprint("report",__name__)

# MySQL configurations
@report_bap.route('/')
def test():
    print ("Will this print")
    return("Will this print")







