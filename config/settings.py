"""
Configuration settings for the application.
Environment variables should be used in production.
"""
import os

# Database Configuration
DATABASE_CONFIG = {
    'charset': 'utf8mb4',
    'connect_timeout': 10,
    'cursorclass': 'pymysql.cursors.DictCursor',
    'db': 'defaultdb',
    'host': os.getenv('DB_HOST', 'mysql-debe0f5-tonyjacobk-250a.j.aivencloud.com'),
    'password': os.getenv('DB_PASSWORD', 'AVNS_8LGmYfYY_PAVDof6hRt'),
    'read_timeout': 10,
    'port': int(os.getenv('DB_PORT', 19398)),
    'user': os.getenv('DB_USER', 'avnadmin'),
    'write_timeout': 10,
}

# Redis Configuration
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'redis-11972.c241.us-east-1-4.ec2.cloud.redislabs.com'),
    'port': int(os.getenv('REDIS_PORT', 11972)),
    'decode_responses': True,
    'username': os.getenv('REDIS_USERNAME', 'default'),
    'password': os.getenv('REDIS_PASSWORD', 'DNqKItilJwjmg6jtLKXQoUlHvSwaOSlP'),
}

# MEGA Configuration
MEGA_CONFIG = {
    'email': os.getenv('MEGA_EMAIL', 'tonyjacobk@gmail.com'),
    'password': os.getenv('MEGA_PASSWORD', 'Simansy@2022'),
}

# Application Configuration
APP_CONFIG = {
    'UPLOAD_FOLDER': '/tmp',
    'ALLOWED_EXTENSIONS': {'txt', 'pdf', 'csv', 'jpg', 'jpeg', 'gif'},
    'ROWS_PER_PAGE': 20,
    'SECTOR_PAGE_SIZE': 50,
    'DEBUG': os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
    'HOST': os.getenv('FLASK_HOST', '0.0.0.0'),
}

# API Request Headers
REQUEST_HEADERS = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# File Paths
FILE_PATHS = {
    'PRICE_CSV': 'price.csv',
    'BSE_CSV': 'bse.csv',
    'DICTPRICE_JSON': 'dictprice.json',
    'PRICE_BACKUP': 'price.bak',
    'BSE_BACKUP': 'bse.bak',
}
