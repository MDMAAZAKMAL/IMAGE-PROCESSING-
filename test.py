# import wx
# import cv2
# import numpy as np
# from PIL import Image
# from collections import Counter

# # ----------------------------
# # Original functions
# # ----------------------------

# def grayscale_and_histogram(image_path):
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # histogram of grayscale
#     hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
#     return gray, hist


# def compare_histograms(hist1, hist2):
#     score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
#     return score


# # ----------------------------
# # WX GUI Class
# # ----------------------------

# class MainFrame(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title="Image Histogram Comparator", size=(900, 600))

#         panel = wx.Panel(self)

#         vbox = wx.BoxSizer(wx.VERTICAL)

#         # Buttons
#         hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
#         self.btn_load1 = wx.Button(panel, label="Load Image 1")
#         self.btn_load2 = wx.Button(panel, label="Load Image 2")
#         self.btn_compare = wx.Button(panel, label="Compare Histograms")

#         hbox_buttons.Add(self.btn_load1, 1, wx.ALL, 5)
#         hbox_buttons.Add(self.btn_load2, 1, wx.ALL, 5)
#         hbox_buttons.Add(self.btn_compare, 1, wx.ALL, 5)

#         # Image Display
#         hbox_images = wx.BoxSizer(wx.HORIZONTAL)
#         self.image_box1 = wx.StaticBitmap(panel, size=(400, 400))
#         self.image_box2 = wx.StaticBitmap(panel, size=(400, 400))

#         hbox_images.Add(self.image_box1, 1, wx.ALL | wx.EXPAND, 5)
#         hbox_images.Add(self.image_box2, 1, wx.ALL | wx.EXPAND, 5)

#         # Result Text
#         self.result_text = wx.StaticText(panel, label="Histogram Score: None", style=wx.ALIGN_CENTER)

#         # Add to main layout
#         vbox.Add(hbox_buttons, 0, wx.CENTER)
#         vbox.Add(hbox_images, 1, wx.EXPAND)
#         vbox.Add(self.result_text, 0, wx.ALL | wx.CENTER, 10)

#         panel.SetSizer(vbox)

#         # Event Binding
#         self.btn_load1.Bind(wx.EVT_BUTTON, self.load_image1)
#         self.btn_load2.Bind(wx.EVT_BUTTON, self.load_image2)
#         self.btn_compare.Bind(wx.EVT_BUTTON, self.compare_images)

#         self.path1 = None
#         self.path2 = None
#         self.gray1 = None
#         self.gray2 = None
#         self.hist1 = None
#         self.hist2 = None

#     # ----------------------------
#     # Utility to show image in StaticBitmap
#     # ----------------------------
#     def display_image(self, path, control):
#         img = Image.open(path)
#         img = img.resize((400, 400))
#         wx_img = wx.Bitmap.FromBufferRGBA(img.size[0], img.size[1], img.convert("RGBA").tobytes())
#         control.SetBitmap(wx_img)

#     # ----------------------------
#     # Load Image 1
#     # ----------------------------
#     def load_image1(self, event):
#         dialog = wx.FileDialog(self, "Choose Image 1", wildcard="*.jpg;*.png")
#         if dialog.ShowModal() == wx.ID_OK:
#             self.path1 = dialog.GetPath()
#             self.display_image(self.path1, self.image_box1)
#             self.gray1, self.hist1 = grayscale_and_histogram(self.path1)

#     # ----------------------------
#     # Load Image 2
#     # ----------------------------
#     def load_image2(self, event):
#         dialog = wx.FileDialog(self, "Choose Image 2", wildcard="*.jpg;*.png")
#         if dialog.ShowModal() == wx.ID_OK:
#             self.path2 = dialog.GetPath()
#             self.display_image(self.path2, self.image_box2)
#             self.gray2, self.hist2 = grayscale_and_histogram(self.path2)

#     # ----------------------------
#     # Compare Histograms
#     # ----------------------------
#     def compare_images(self, event):
#         if self.hist1 is None or self.hist2 is None:
#             wx.MessageBox("Load both images first!", "Error", wx.ICON_ERROR)
#             return

#         score = compare_histograms(self.hist1, self.hist2)
#         self.result_text.SetLabel(f"Histogram Score: {score:.4f}")


# # ----------------------------
# # Run App
# # ----------------------------
# if __name__ == "__main__":
#     app = wx.App()
#     frame = MainFrame()
#     frame.Show()
#     app.MainLoop()


'''

import wx
from PIL import Image
import cv2
import numpy as np

paths = []   # store image paths globally

# -------------------------------
#   BUTTON 1: Select images
# -------------------------------
def choose_image(event):
    global paths
    wildcard = "Image files (.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    dialog = wx.FileDialog(None, "Select images", wildcard=wildcard,
                           style=wx.FD_MULTIPLE)

    if dialog.ShowModal() == wx.ID_OK:
        paths = dialog.GetPaths()

    dialog.Destroy()


# -------------------------------
#   BUTTON 2: Convert to Greyscale
# -------------------------------
def to_greyscale(event):
    for path in paths:
        img = Image.open(path)
        grey = img.convert("L")
        grey.show()


# -------------------------------
#   BUTTON 3: Count Red Pixels
# -------------------------------
def count_red_pixels(event):
    if not paths:
        print("No images selected!")
        return

    for path in paths:
        img = cv2.imread(path)

        if img is None:
            print("Could not load:", path)
            continue

        # BGR → HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Two red ranges
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        red_mask = mask1 + mask2

        red_pixels = cv2.countNonZero(red_mask)
        print(f"{path} → Red pixels = {red_pixels}")

        # Show masked image
        red_highlight = cv2.bitwise_and(img, img, mask=red_mask)
        cv2.imshow("Red Pixels", red_highlight)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# ==================================
#          GUI LAYOUT
# ==================================
app = wx.App()
frame = wx.Frame(None, title="Jackfruit Problem", size=(500, 700))
panel = wx.Panel(frame)
panel.SetBackgroundColour("#F4EC94")

font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
title = wx.StaticText(panel, label="Picture Tools", pos=(20, 30))
title.SetFont(font)

# Button container panel
inner_panel = wx.Panel(panel, pos=(0, 350), size=(500, 200))

btn1 = wx.Button(inner_panel, label="Select Image(s)")
btn2 = wx.Button(inner_panel, label="Convert to Greyscale")
btn3 = wx.Button(inner_panel, label="Count Red Pixels")

# Bind buttons
btn1.Bind(wx.EVT_BUTTON, choose_image)
btn2.Bind(wx.EVT_BUTTON, to_greyscale)
btn3.Bind(wx.EVT_BUTTON, count_red_pixels)

# Sizer for 3 buttons
sizer = wx.GridSizer(1, 3, 50, 50)
sizer.Add(btn1, 1, wx.EXPAND)
sizer.Add(btn2, 1, wx.EXPAND)
sizer.Add(btn3, 1, wx.EXPAND)

inner_panel.SetSizerAndFit(sizer)

frame.Show()
app.MainLoop()

'''


import wx

app = wx.App()

frame = wx.Frame(None, title="Bitmap Example", size=(400,300))
panel = wx.Panel(frame)

bmp = wx.Bitmap("cat.jpg", wx.BITMAP_TYPE_JPEG)

img_ctrl = wx.StaticBitmap(panel, bitmap=bmp)

sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(img_ctrl, 0, wx.ALL, 20)

panel.SetSizer(sizer)

frame.Show()
app.MainLoop()

