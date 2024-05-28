'''
Author: M1tsuha
Date: 2024-05-06 14:02:49
LastEditors: M1tsuha
LastEditTime: 2024-05-06 17:30:31
FilePath: \prac3_506\geohash.py
Description: 

Copyright (c) 2024 by 1300935620@qq.com, All Rights Reserved. 
'''

def encode_geohash(longitude, latitude, precision):
    """
    将经纬度编码为指定精度的GeoHash字符串。
    
    参数:
    longitude - 经度，浮点数。
    latitude - 纬度，浮点数。
    precision - 编码精度，即生成的GeoHash字符串的长度。
    
    返回值:
    编码后的GeoHash字符串。
    """
    base32_map = "0123456789bcdefghjkmnpqrstuvwxyz"  # base32编码字符集
    min_lat, max_lat = -90.0, 90.0  # 纬度的范围
    min_lon, max_lon = -180.0, 180.0  # 经度的范围
    geohash = []  # 用于存储生成的GeoHash字符串
    bit = 0  # 当前处理的bit位
    ch = 0  # 用于存储5个bit位转换后的base32字符的索引
    bit_length = 0  # 已处理的bit位长度

    while len(geohash) < precision:  # 循环直到达到指定的精度
        if bit_length % 2 == 0:  # 处理偶数位，编码经度
            mid = (min_lon + max_lon) / 2  
            if longitude > mid:  # 如果当前经度在二分范围右侧
                ch |= 1 << (4 - bit)  
                # ch初始化为00000 位于二分右侧则当前位记1
                # 即左移4-bit位 标记对应的bit位
                min_lon = mid  # 更新经度范围的左边界
                
            else:  # 经度在二分范围左侧
                max_lon = mid  # 更新经度范围的右边界
                
        else:  # 处理奇数位，编码纬度
            mid = (min_lat + max_lat) / 2  
            if latitude > mid:  # 如果当前纬度在二分范围右侧
                ch |= 1 << (4 - bit)  # 标记对应的bit位
                min_lat = mid  
            else:  
                max_lat = mid  
        
        bit += 1  # 移动到下一个bit位
        bit_length += 1  # 更新已处理的bit位长度

        if bit == 5:  # 每5个bit位转换为一个base32字符
            geohash.append(base32_map[ch])  # 添加base32字符到结果中
            bit = 0  # 重置bit位计数器
            ch = 0  # 重置base32索引

    return ''.join(geohash)  # 将结果中的字符连接成字符串

# 计算不同长度的GeoHash编码
coords = (115.83122,37.49867)  # 经度，纬度
lengths = [8, 9, 10]

for length in lengths:
    print(f'{length}-bit GeoHash: {encode_geohash(coords[0], coords[1], length)}')
