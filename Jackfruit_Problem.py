import cv2
import numpy as np
from PIL import Image
from collections import Counter

# ------------------------------------------
# 1. COUNT RED PIXELS + FIND DOMINANT COLOR
# ------------------------------------------

def count_red_pixels(image):
    # Convert BGR (OpenCV) to HSV for color filtering
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Lower and upper ranges for RED color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2
    red_pixels = cv2.countNonZero(mask)

    return red_pixels


def get_dominant_color(image_path):
    img = Image.open(image_path)
    img = img.resize((100, 100))        # reduce size for faster processing
    img = img.convert("RGB")

    colors = img.getdata()
    most_common = Counter(colors).most_common(1)[0][0]

    return most_common   # (R, G, B)


# ------------------------------------------
# 2. GRAYSCALE + HISTOGRAM DIFFERENCE
# ------------------------------------------

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

# ------------------------------------------
# MAIN TESTING
# ------------------------------------------

image_path1 = "image1.jpg"
image_path2 = "image2.jpg"

# Load images
img1 = cv2.imread(image_path1)
img2 = cv2.imread(image_path2)

# 1. RED PIXELS + DOMINANT COLOR
red_count = count_red_pixels(img1)
dominant_color = get_dominant_color(image_path1)

print(f"Red pixels in image1: {red_count}")
print(f"Dominant color in image1 (R,G,B): {dominant_color}")

# 2. GRAYSCALE + HISTOGRAM DIFFERENCE
gray1, hist1 = grayscale_and_histogram(image_path1)
gray2, hist2 = grayscale_and_histogram(image_path2)

hist_score = compare_histograms(hist1, hist2)
print(f"Histogram similarity score: {hist_score}")

# Show results
cv2.imshow("Gray1", gray1)
cv2.imshow("Gray2", gray2)
cv2.waitKey(0)
cv2.destroyAllWindows()