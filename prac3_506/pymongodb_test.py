'''
Author: M1tsuha
Date: 2024-05-06 15:26:26
LastEditors: M1tsuha
LastEditTime: 2024-05-06 16:21:06
FilePath: \Learning-Geospatial-Analysis-with-Python-Third-Edition\pymongodb_test.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
from pymongo import MongoClient

# 连接到 MongoDB
client = MongoClient('localhost', 27017)
db = client['china']  # 使用你的数据库名称
collection = db['shp']  # 使用你的集合名称

# 定义直线的两点
line = {
    "type": "LineString",
    "coordinates": [
        [84.06, 26.18],  # 起点坐标
        [109.56, 46.02]  # 终点坐标
    ]
}

# 执行查询，查找与直线相交的地理对象
query_result = collection.find({
    "geometry": {
        "$geoIntersects": {
            "$geometry": line
        }
    }
})

# 打印结果，排除地理坐标信息
for doc in query_result:
    print({key: value for key, value in doc.items() if key != 'geometry'})
