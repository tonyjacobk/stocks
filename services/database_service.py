"""
Database service for MySQL operations.
Provides connection management and common database operations.
"""
import logging
from math import ceil
from datetime import datetime, timedelta
import pymysql
from config.settings import DATABASE_CONFIG

logger = logging.getLogger(__name__)


def get_connection():
    """Create and return a database connection."""
    try:
        connection = pymysql.connect(**DATABASE_CONFIG)
        return connection
    except pymysql.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def check_row_exists(cursor, broker, company, date):
    """Check if a row exists in the reports table."""
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM reports
            WHERE broker = %s AND company = %s AND report_date = %s
        ) AS row_exists
    """
    cursor.execute(query, (broker, company, date))
    result = cursor.fetchone()
    return result['row_exists'] if result else False


def find_rows_by_recommendation(recom, broker, target):
    """Find rows matching recommendation, broker, and target."""
    query = """
        SELECT *
        FROM reports
        WHERE recommendation = %s AND broker = %s AND target = %s
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (recom, broker, target))
    found = list(cursor)
    cursor.close()
    connection.close()
    return found


def get_paginated_rows(page_no, per_page=20):
    """Get paginated rows from reports table."""
    connection = get_connection()
    cursor = connection.cursor()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) as total FROM reports")
    total_rows = cursor.fetchone()['total']
    total_pages = ceil(total_rows / per_page)
    
    # Get data for current page
    offset = (page_no - 1) * per_page
    cursor.execute(
        "SELECT * FROM reports ORDER BY report_date DESC, broker LIMIT %s OFFSET %s",
        (per_page, offset)
    )
    data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return data, total_pages


def get_rows_by_broker(page_no, per_page, broker):
    """Get paginated rows filtered by broker."""
    connection = get_connection()
    cursor = connection.cursor()
    
    broker_pattern = f"%{broker}%"
    
    # Get total count
    cursor.execute(
        "SELECT COUNT(*) as total FROM reports WHERE broker LIKE %s",
        (broker_pattern,)
    )
    total_rows = cursor.fetchone()['total']
    total_pages = ceil(total_rows / per_page)
    
    # Get data for current page
    offset = (page_no - 1) * per_page
    cursor.execute(
        """SELECT * FROM reports 
           WHERE broker LIKE %s 
           ORDER BY report_date DESC 
           LIMIT %s OFFSET %s""",
        (broker_pattern, per_page, offset)
    )
    data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return data, total_pages


def get_rows_by_stock(page_no, per_page, stock):
    """Get paginated rows filtered by exact stock/company name."""
    connection = get_connection()
    cursor = connection.cursor()
    
    # Get total count
    cursor.execute(
        "SELECT COUNT(*) as total FROM reports WHERE company = %s",
        (stock,)
    )
    total_rows = cursor.fetchone()['total']
    total_pages = ceil(total_rows / per_page)
    
    # Get data for current page
    offset = (page_no - 1) * per_page
    cursor.execute(
        """SELECT * FROM reports 
           WHERE company = %s 
           ORDER BY report_date DESC 
           LIMIT %s OFFSET %s""",
        (stock, per_page, offset)
    )
    data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return data, total_pages


def get_rows_by_stock_partial(page_no, per_page, stock):
    """Get paginated rows filtered by partial stock/company name match."""
    connection = get_connection()
    cursor = connection.cursor()
    
    stock_pattern = f"%{stock}%"
    
    # Get total count
    cursor.execute(
        "SELECT COUNT(*) as total FROM reports WHERE company LIKE %s",
        (stock_pattern,)
    )
    total_rows = cursor.fetchone()['total']
    total_pages = ceil(total_rows / per_page)
    
    # Get data for current page
    offset = (page_no - 1) * per_page
    cursor.execute(
        """SELECT * FROM reports 
           WHERE company LIKE %s 
           ORDER BY report_date DESC 
           LIMIT %s OFFSET %s""",
        (stock_pattern, per_page, offset)
    )
    data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return data, total_pages


def check_company_broker_date_range(conn, company, broker, date_str):
    """
    Check if company-broker combination exists within ±10 days of given date.
    
    Returns:
        tuple: (exists: bool, rows: list)
    """
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = (base_date - timedelta(days=10)).date()
    end_date = (base_date + timedelta(days=10)).date()

    query = """
        SELECT *
        FROM reports
        WHERE company = %s
          AND broker = %s
          AND report_date BETWEEN %s AND %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (company, broker, start_date, end_date))
    rows = cursor.fetchall()

    if rows:
        return True, rows
    return False, []


def add_company_report(company, broker, url, report_date, recommendation, 
                       target, site, nsekey):
    """Add a new company report to the database."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO reports
        (company, broker, URL, report_date, recommendation, target, site, NSEKEY)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (company, broker, url, report_date, recommendation, target, site, nsekey))

    connection.commit()
    cursor.close()
    connection.close()
