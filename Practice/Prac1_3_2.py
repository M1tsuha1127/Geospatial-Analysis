# Get mongodb query efficiency.

'''
Author: M1tsuha
Date: 2024-06-15 18:24:59
LastEditors: M1tsuha
LastEditTime: 2024-06-16 02:12:15
FilePath: \Geospatial-Analysis\Practice\Prac1_3_2.py
Description: Get mongodb query efficiency.

Copyright (c) 2024 by WHURS_M1tsuha, All Rights Reserved. 
'''

from pymongo import MongoClient, GEOSPHERE
import time

# 连接到 MongoDB 数据库
print("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
db = client["test"]  
collection = db["niuchiyuan"]
print("Connected to MongoDB.")

# 创建空间索引
#collection.create_index([("geometry","2dsphere")])

# 查询命令
query = {
    "geometry": {
        "$geoIntersects": {
            "$geometry": {
                "type": "LineString",
                "coordinates": [[112.1, 32.23], [113.98, 30.63], [115.05, 30.42]]
            }
        }
    }
}

# 执行查询记录时间
times = []
for i in range(5):
    start_time = time.time()
    results = list(collection.find(query))
    end_time = time.time()
    times.append(end_time - start_time)
    print(f"Query {i+1} executed in {times[-1]:.4f} seconds.")

average_time = sum(times) / len(times)
print(f"Average query time with index: {average_time:.4f} seconds.")
