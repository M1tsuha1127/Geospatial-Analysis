# Get postgis query efficiency.

'''
Author: M1tsuha
Date: 2024-06-15 18:16:19
LastEditors: M1tsuha
LastEditTime: 2024-06-16 01:11:35
FilePath: \Geospatial-Analysis\Practice\Prac1_3_1.py
Description: Get postgis query efficiency.

Copyright (c) 2024 by WHURS_M1tsuha, All Rights Reserved. 
'''

import psycopg2
import time

# 连接到 PostgreSQL 数据库
print("Connecting to PostgreSQL...")
conn = psycopg2.connect(
    dbname="test",  
    user="postgres",      
    password="123456",     
    host="localhost"       
)
cur = conn.cursor()
print("Connected to PostgreSQL.")

# 创建空间索引
cur.execute("CREATE INDEX IF NOT EXISTS idx_niuchiyuan_geom ON niuchiyuan USING GIST (geom);")
conn.commit()

# 查询命令
query = """
SELECT * FROM niuchiyuan
WHERE ST_Intersects(geom, ST_GeomFromText('LINESTRING(112.1 32.23, 113.98 30.63, 115.05 30.42)', 4326));
"""

# 执行查询记录时间
times = []
for i in range(5):
    start_time = time.time()
    cur.execute(query)
    results = cur.fetchall()
    end_time = time.time()
    times.append(end_time - start_time)
    print(f"Query {i+1} executed in {times[-1]:.4f} seconds.")

cur.close()
conn.close()

# 平均时间
average_time = sum(times) / len(times)
print(f"Average query time: {average_time:.4f} seconds.")
