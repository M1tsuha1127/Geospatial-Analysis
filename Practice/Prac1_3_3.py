# Get postgis query result.

'''
Author: M1tsuha
Date: 2024-06-15 18:42:59
LastEditors: M1tsuha
LastEditTime: 2024-06-16 01:46:34
FilePath: \Geospatial-Analysis\Practice\Prac1_3_3.py
Description: Get postgis query result.

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''

import psycopg2

# 连接到 PostgreSQL 数据库
print("Connecting to PostgreSQL...")
conn = psycopg2.connect(
    dbname="test",  # 替换为您的数据库名称
    user="postgres",        # 替换为您的用户名
    password="123456",      # 替换为您的密码
    host="localhost"        # 替换为您的主机名
)
cur = conn.cursor()
print("Connected to PostgreSQL.")

# 查询命令，统计合计面积与建筑物数量
query = """
SELECT COUNT(*), SUM(ST_Area(ST_Transform(geom, 9479))) AS total_area
FROM niuchiyuan
WHERE ST_Intersects(geom, ST_GeomFromText('LINESTRING(112.1 32.23, 113.98 30.63, 115.05 30.42)', 4326));
"""

# 执行查询，并计算平均面积
cur.execute(query)
count, total_area = cur.fetchone()
if count > 0:
    avg_area = total_area / count
else:
    avg_area = 0

# 打印输出结果
print(f"Total buildings: {count}")
print(f"Total area (sq m): {total_area:.2f}")
print(f"Average building area (sq m): {avg_area:.2f}")

cur.close()
conn.close()
