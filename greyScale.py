import cv2
import numpy as np
from PIL import Image
from collections import Counter

def grayscale_and_histogram(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # histogram of grayscale
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    return gray, hist


def compare_histograms(hist1, hist2):
    # Correlation is a good comparison technique
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return score

image_path1 = "cat.jpg"
image_path2 = "image2.jpg"

# Load images
img1 = cv2.imread(image_path1)
img2 = cv2.imread(image_path2)

gray1, hist1 = grayscale_and_histogram(image_path1)
gray2, hist2 = grayscale_and_histogram(image_path2)

hist_score = compare_histograms(hist1, hist2)
print(f"Histogram similarity score: {hist_score}")

# Show results 
cv2.imshow("Gray1", gray1)
cv2.imshow("Gray2", gray2)
cv2.waitKey(0)
cv2.destroyAllWindows()