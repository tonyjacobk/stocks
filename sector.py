from flask import Flask, render_template, request, redirect, url_for,Blueprint
from aiven import get_rows,get_broker,connect
import urllib.parse
import math
from megclass import MegaMan
sector_bp=Blueprint("sector",__name__)

# Database configuration

def get_connection():
  return connect()
@sector_bp.route('/')
@sector_bp.route('/<int:page>')
@sector_bp.route('/filter/<key>/<value>/<int:page>')
def index(key=None, value=None, page=1):
    conn = get_connection()
    cursor = conn.cursor()

    page_size = 50
    offset = (page - 1) * page_size

    # Get search parameters
    search_by_broker = request.args.get('search_by_broker', '')
    search_by_company = request.args.get('search_by_company', '')

    # Base query
    base_query = "FROM gen_reports"
    conditions = []
    params = []

    if key and value:
        conditions.append(f"{key} = %s")
        params.append(value)

    if search_by_broker:
        conditions.append("broker LIKE %s")
        params.append(f"%{search_by_code}%")

    if search_by_company:
        conditions.append("company LIKE %s")
        params.append(f"%{search_by_company}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # Get total number of rows for pagination
    count_query = "SELECT COUNT(*) " + base_query + where_clause
    cursor.execute(count_query, tuple(params))
    total_rows = cursor.fetchone()['COUNT(*)']
    total_pages = math.ceil(total_rows / page_size)

    # Get data for the current page
    data_query = "SELECT * " + base_query + where_clause + f" LIMIT %s OFFSET %s"
    params.extend([page_size, offset])
    cursor.execute(data_query, tuple(params))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('sectorindex.html',
                           rows=rows,
                           page=page,
                           total_pages=total_pages,
                           key=key,
                           value=value,
                           search_by_broker=search_by_broker,
                           search_by_company=search_by_company)

@sector_bp.route('/delete', methods=['POST'])
def delete():
    print ("In delete")
    company = request.form["company"]
    broker = request.form['broker']
    report_date = request.form['date']
    URL=request.form["URL"]
    conn = get_connection()
    cursor = conn.cursor()
    print(company,broker,report_date)
    print(URL)
    cursor.execute("""
        DELETE FROM gen_reports 
        WHERE company=%s  AND report_date=%s
    """, (company, report_date))
    print(URL)
    MegaMan.delete_url(URL)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('sector.index'))

@sector_bp.route('/save', methods=['POST'])
def save():
    data = (
        request.form['company'],
        request.form['broker'],
        request.form['URL'],
        request.form['date'],
        request.form['site'],
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        REPLACE INTO reports 
        (company, broker, URL,  report_date, site) 
        VALUES (%s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('sector.index'))
@sector_bp.route('/move', methods=['POST'])
def move():
    print ("In Move")
    company = request.form['company']
    broker = request.form['broker']
    report_date = request.form['date']
    URL=request.form["URL"]
    conn = get_connection()
    cursor = conn.cursor()
    print(company,broker,report_date)
    cursor.execute("""
        UPDATE  gen_reports SET Site = %s
        WHERE company=%s  AND report_date=%s
    """, ("mv",company, report_date))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('sector.index'))

