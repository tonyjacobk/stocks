from flask import Flask, render_template
import pymysql
from aiven import connect
from math import ceil

app = Flask(__name__)

# MySQL configurations
mysql=connect()
@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 20
    cur = mysql.cursor()
    cur.execute("SELECT COUNT(*) FROM reports")
    total_rows = cur.fetchone()['COUNT(*)']
    print(total_rows)
    total_pages = ceil(total_rows / per_page)
    offset = (page - 1) * per_page
    print (offset)
    cur.execute(f"SELECT * FROM reports ORDER BY report_date DESC  LIMIT 20 OFFSET ?", (offset,) )
    data = cur.fetchall()
    print (data)
    cur.close()
    return render_template('index.html', data=data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


