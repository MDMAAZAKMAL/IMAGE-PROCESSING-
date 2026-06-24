
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def histogram_difference(paths):
    # ---- SELECT IMAGES HERE ----
    img1_path = paths[0]
    img2_path = paths[1]

    # Load images in grayscale
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    if img1 is None or img2 is None:
        print("Error: One or both images not found.")
        exit()

    # Compute histograms
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

    # Histogram difference
    difference = np.abs(hist1 - hist2).sum()

    print("\n====================================")
    print("Histogram Difference:", difference)
    print("====================================\n")

    # Plot histograms
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.title("Histogram - Image 1")
    plt.plot(hist1, color='black')

    plt.subplot(1, 2, 2)
    plt.title("Histogram - Image 2")
    plt.plot(hist2, color='black')

    plt.tight_layout()
    plt.show()
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import wx


def histogram_difference(paths, panel3):
    img1_path = paths[0]
    img2_path = paths[1]

    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    if img1 is None or img2 is None:
        wx.MessageBox("Error: One or both images not found.")
        return

    # Histograms
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    diff = np.abs(hist1 - hist2).sum()

    # ---------------------------
    # Create matplotlib figure
    # ---------------------------
    fig = plt.figure(figsize=(5, 3), dpi=100)

    ax1 = fig.add_subplot(121)
    ax1.set_title("Image 1")
    ax1.plot(hist1, color='black')

    ax2 = fig.add_subplot(122)
    ax2.set_title("Image 2")
    ax2.plot(hist2, color='black')

    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    w, h = fig.get_size_inches() * fig.get_dpi()
    w, h = int(w), int(h)

    # FIX: convert buffer → numpy array
    buf = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    buf = buf.reshape((h, w, 4))

    wx_img = wx.Image(w, h)
    wx_img.SetData(buf[:, :, :3].tobytes())   # RGB
    wx_img.SetAlpha(buf[:, :, 3].tobytes())   # Alpha
    bmp = wx.Bitmap(wx_img)

    plt.close(fig)

    # ---------------------------
    # APPEND to Panel 3 (NO CLEAR)
    # ---------------------------
    if not panel3.GetSizer():
        panel3.SetSizer(wx.BoxSizer(wx.VERTICAL))

    # Add text
    diff_text = wx.StaticText(panel3, label=f"Histogram Difference = {diff}")
    panel3.GetSizer().Add(diff_text, 0, wx.ALL, 5)

    # Add histogram image
    bmp_ctrl = wx.StaticBitmap(panel3, bitmap=bmp)
    panel3.GetSizer().Add(bmp_ctrl, 0, wx.ALL, 5)

    panel3.Layout()
