'''
Author: M1tsuha
Date: 2024-06-15 18:11:09
LastEditors: M1tsuha
LastEditTime: 2024-06-16 01:49:20
FilePath: \Geospatial-Analysis\Practice\Prac1_1.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import psycopg2
import os
from osgeo import ogr

# 连接到数据库
print("Connecting to PostgreSQL...")
conn = psycopg2.connect(
    dbname="m1tsuha",  
    user="postgres",    
    password="123456",     
    host="localhost"  
)
cur = conn.cursor()
print("Connected to PostgreSQL.")

# 设置 Shapefile 编码为 UTF-8
os.environ['SHAPE_ENCODING'] = "UTF-8"

# 执行空间查询，找出位于湖北省范围内的建筑物
query = """
SELECT b.*
FROM buildings b, china c
WHERE c.name = '湖北省' 
  AND ST_Within(ST_GeomFromWKB(b.wkb_geometry, 4326), ST_GeomFromWKB(c.wkb_geometry, 4326));
"""
cur.execute(query)

# 使用 GDAL 创建 Shapefile 并写入查询结果
driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.CreateDataSource('Practice/data/hubei/hubei.shp')  # 创建 Shapefile
layer = ds.CreateLayer('hubei', geom_type=ogr.wkbPolygon)  # 创建图层

# 定义属性字段id name type
field_def_id = ogr.FieldDefn("id", ogr.OFTInteger)
layer.CreateField(field_def_id)

field_def_name = ogr.FieldDefn("name", ogr.OFTString)
field_def_name.SetWidth(100)
layer.CreateField(field_def_name)

field_def_type = ogr.FieldDefn("type", ogr.OFTString)
field_def_type.SetWidth(100)
layer.CreateField(field_def_type)

# 获取结果写入Shapefile并获取行数
count = 0
for row in cur:
    geom = ogr.CreateGeometryFromWkb(row[1])
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(geom)

    feature.SetField("id", row[2])
    feature.SetField("name", row[5])
    feature.SetField("type", row[6])

    layer.CreateFeature(feature)

    feature.Destroy()
    count += 1

# 输出建筑物数量
print(f"Number of buildings in Hubei Province: {count}")

# 清理资源
ds.Destroy()
cur.close()
conn.close()
