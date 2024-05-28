from osgeo import gdal_array
import numpy as np
import random

# Load the image into numpy using gdal
src = "GF1.jpg"
srcArr = gdal_array.LoadFile(src)

# Function to classify and save image
def classify_and_save(num_classes, tgt):
    # Split the histogram into num_classes bins as our classes
    classes = np.histogram(srcArr, bins=num_classes)[1]

    # Generate random color look-up table (LUT)
    lut = [[random.randint(0, 255), random.randint(0, 255)
            , random.randint(0, 255)] for _ in range(num_classes + 1)]

    # Starting value for classification
    start = 1

    # Set up the RGB color JPEG output image
    rgb = np.zeros((3, srcArr.shape[0], srcArr.shape[1]), np.float32)

    # Process all classes and assign colors
    for i in range(len(classes)):
        mask = np.logical_and(start <= srcArr, srcArr <= classes[i])
        for j in range(len(lut[i])):
            rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
        start = classes[i] + 1

    # Save the image
    output = gdal_array.SaveArray(rgb.astype(np.uint8), tgt, format="JPEG")
    output = None

# Classify and save images with 5, 10, and 15 classes
classify_and_save(5, "classified_5_classes.jpg")
classify_and_save(10, "classified_10_classes.jpg")
classify_and_save(15, "classified_15_classes.jpg")
