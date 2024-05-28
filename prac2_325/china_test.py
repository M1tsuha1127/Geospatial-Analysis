# Rasterize a shapefile with PIL

# https://github.com/GeospatialPython/Learning/raw/master/hancock.zip
import PIL
from PIL import Image
from PIL import ImageDraw
import shapefile
import random

r = shapefile.Reader("china_shp/china.shp")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 3000
iheight = int(iwidth / xdist * ydist)
xratio = iwidth / xdist
yratio = iheight / ydist

img = Image.new("RGB", (iwidth, iheight), "white")
draw = ImageDraw.Draw(img)

for shape in r.shapes():
    # Initialize an empty list to store polygons for this shape
    shape_polys = []

    # Keep track of the last part's end index
    last_part_end_index = 0

    # Iterate over the parts array.  part_index:0,1,2,3...  start_index:第part_index的起始索引，end_index:第part_index+1的起始索引
    for part_index in range(len(shape.parts)):#循环遍历parts（是一个列表，将点集合组合为形状，如果形状具有多个部分，则显示的是每个部分的第一点索引。）
        start_index = shape.parts[part_index]#记录当前shape中某个part的起始索引
        if part_index < len(shape.parts) - 1:#如果不是最后一个part
            end_index = shape.parts[part_index + 1]#记录当前shape某个part的结束索引
        else:
            # For the last part, use the total number of points
            end_index = len(shape.points)

        # Extract the points belonging to the current part
        part_points = shape.points[start_index:end_index]

        # Convert map coordinates to pixel coordinates and store them in a new list
        part_pixels = [(int(iwidth - ((r.bbox[2] - x) * xratio)), int((r.bbox[3] - y) * yratio)) for x, y in part_points]

        # Append the part's pixels to the list of polygons for this shape
        shape_polys.append(part_pixels)

        # Draw the polygon using the stored pixel coordinates
        if len(part_pixels) > 2:
            fill_color_r = int(255 * random.random())
            fill_color_g = int(255 * random.random())
            fill_color_b = int(255 * random.random())
            draw.polygon(part_pixels, outline="rgb(20,20,20)", fill=f"rgb({fill_color_r},{fill_color_g},{fill_color_b})")

    # Continue with the next shape in the Shapefile

img.save("Output/result.png")