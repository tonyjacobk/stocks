import pymysql
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from math import ceil

timeout = 10
def connect():
 connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysql-debe0f5-tonyjacobk-250a.j.aivencloud.com",
  password="AVNS_8LGmYfYY_PAVDof6hRt",
  read_timeout=timeout,
  port=19398,
  user="avnadmin",
  write_timeout=timeout,
)
 return connection

def row_exists(broker,company,date):
    query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM {table_name}
            WHERE broker = %s AND company = %s AND report_date = %s
        ) AS row_exists
    """

    cursor.execute(query, (broker,company,date))
    result = cursor.fetchone()
def row_exists_no_comp(broker,recom,target):
    found=[]
    query = f"""
            SELECT *
            FROM reports
            WHERE  recommendation = %s AND broker =%s AND target = %s
    """
    connection=connect()
    cursor=connection.cursor()
    cursor.execute(query, (recom,broker,target))
    for row in cursor:
     found.append(row)
    return (found)


def get_rows(pageNo,per_page):
    mysql=connect()
    cursor=mysql.cursor()
    per_page = 20
    cur = mysql.cursor()
    cur.execute("SELECT COUNT(*) FROM reports")
    total_rows = cur.fetchone()['COUNT(*)']
    total_pages = ceil(total_rows / per_page)
    offset = (pageNo - 1) * per_page
    cur.execute(f"SELECT * FROM reports ORDER BY report_date DESC,broker  LIMIT 20 OFFSET %s", (offset) )
    data = cur.fetchall()
    cursor.close()
    return data,total_pages
def get_broker(pageNo,per_page,broker):
    mysql=connect()
    cursor=mysql.cursor()
    per_page = 20
    cur = mysql.cursor()
    cur.execute("SELECT COUNT(*) FROM reports where broker= %s",(broker))
    total_rows = cur.fetchone()['COUNT(*)']
    total_pages = ceil(total_rows / per_page)
    offset = (pageNo - 1) * per_page
    cur.execute(f"SELECT * FROM reports where broker = %s ORDER BY report_date DESC  LIMIT 20 OFFSET %s", (broker,offset) )
    data = cur.fetchall()
    cursor.close()
    return data,total_pages

