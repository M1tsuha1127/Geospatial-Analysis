'''
Author: M1tsuha
Date: 2024-06-16 02:40:15
LastEditors: M1tsuha
LastEditTime: 2024-06-16 02:42:54
FilePath: \Geospatial-Analysis\Practice\Prac2_1.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, osr

def read_tiff(file_path):
    ds = gdal.Open(file_path)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    gt = ds.GetGeoTransform()
    return arr, gt, ds

def flood_analysis(elevation_data, gt, flood_points, flood_elevation=2500):
    out_data = np.zeros_like(elevation_data)
    for point in flood_points:
        # Transform geographic coordinates to raster coordinates
        px = int((point[0] - gt[0]) / gt[1])
        py = int((point[1] - gt[3]) / gt[5])
        # Mark as flooded if the elevation is less than or equal to the flood elevation
        out_data[elevation_data <= flood_elevation] = 1
    return out_data

def export_to_asc(array, output_path):
    np.savetxt(output_path, array, fmt='%d', delimiter=' ')

def plot_overlay(original_data, flood_data):
    plt.figure(figsize=(10, 8))
    plt.imshow(original_data, cmap='gray')
    plt.imshow(flood_data, cmap='Reds', alpha=0.5)
    plt.colorbar()
    plt.show()

# File paths and flood points
file_path = 'Practice/data/s51/s51.tif'
output_asc = 'Practice/data/s51/flooded_area.asc'
flood_points = [(71.497, 39.267), (74.67, 35.73)]  # (Longitude, Latitude)

# Process data
elevation_data, geo_transform, dataset = read_tiff(file_path)
flood_map = flood_analysis(elevation_data, geo_transform, flood_points)
export_to_asc(flood_map, output_asc)
plot_overlay(elevation_data, flood_map)
