from flask import Flask, render_template, request, redirect, url_for
from aiven import get_rows,get_broker,connect
import urllib.parse

app = Flask(__name__)

# Database configuration

def get_connection():
  return connect()
@app.route('/')
@app.route('/filter/<key>/<value>')
def index(key=None, value=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM reports"
    if key and value:
        query += f" WHERE {key} = %s"
        cursor.execute(query, (value,))
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('crudindex.html', rows=rows)

@app.route('/delete', methods=['POST'])
def delete():
    company = request.form['company']
    broker = request.form['broker']
    report_date = request.form['report_date']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM reports 
        WHERE company=%s AND broker=%s AND report_date=%s
    """, (company, broker, report_date))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    data = (
        request.form['company'],
        request.form['broker'],
        request.form['URL'],
        request.form['recommendation'],
        request.form['target'],
        request.form['report_date'],
        request.form['site']
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        REPLACE INTO reports 
        (company, broker, URL, recommendation, target, report_date, site) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

