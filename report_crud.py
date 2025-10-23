from flask import Flask, render_template, request, redirect, url_for,Blueprint
from aiven import get_rows,get_broker,connect
import urllib.parse
import math
crud_bp=Blueprint("crud",__name__)

# Database configuration

def get_connection():
  return connect()
@crud_bp.route('/')
@crud_bp.route('/<int:page>')
@crud_bp.route('/filter/<key>/<value>/<int:page>')
def index(key=None, value=None, page=1):
    conn = get_connection()
    cursor = conn.cursor()

    page_size = 50
    offset = (page - 1) * page_size

    # Get search parameters
    search_by_code = request.args.get('search_by_code', '')
    search_by_company = request.args.get('search_by_company', '')

    # Base query
    base_query = "FROM reports"
    conditions = []
    params = []

    if key and value:
        conditions.append(f"{key} = %s")
        params.append(value)

    if search_by_code:
        conditions.append("NSEKEY LIKE %s")
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

    return render_template('crudindex.html',
                           rows=rows,
                           page=page,
                           total_pages=total_pages,
                           key=key,
                           value=value,
                           search_by_code=search_by_code,
                           search_by_company=search_by_company)

@crud_bp.route('/delete', methods=['POST'])
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
    return redirect(url_for('crud.index'))

@crud_bp.route('/save', methods=['POST'])
def save():
    data = (
        request.form['company'],
        request.form['broker'],
        request.form['URL'],
        request.form['recommendation'],
        request.form['target'],
        request.form['report_date'],
        request.form['site'],
        request.form['code']
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        REPLACE INTO reports 
        (company, broker, URL, recommendation, target, report_date, site,NSEKEY) 
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
    """, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('crud.index'))

