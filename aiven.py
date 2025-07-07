import pymysql
from datetime import datetime

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
