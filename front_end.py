import wx
import countRedPixels
import detectObjects
import detectDominantColour
import histogram
from PIL import Image

def choose_image(event):
    global paths
    paths = []
    wildcard = "Image files(.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    choose_window = wx.FileDialog(None, "Select an image",wildcard = wildcard, style=wx.FD_MULTIPLE)
    if choose_window.ShowModal() == wx.ID_OK:#checks whether i clicked ok 
        paths = choose_window.GetPaths()#list
    choose_window.Destroy()


def to_greyscale(event):

    panel2.DestroyChildren()#to remove the previous used picture if any 

    sizer1 = wx.GridSizer(7, 2, 10, 10)
    font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
    text1 = wx.StaticText(panel2,label = "Converted to GreyScale")
    text1.SetFont(font)
    sizer1.Add(text1,0,wx.ALL,5)
    empty = wx.StaticText(panel2, label="")
    sizer1.Add(empty, 0, wx.EXPAND | wx.ALL,5)

    for path in paths:
        pil_img = Image.open(path)
        grey = pil_img.convert("L")# Grayscale PIL image
        wx_img = wx.Image(grey.size[0], grey.size[1])# Convert to wx.Image
        wx_img.SetData(grey.convert("RGB").tobytes())
        wx_img = wx_img.Scale(300, 200)

        bmp = wx.Bitmap(wx_img)
        img_ctrl = wx.StaticBitmap(panel2, bitmap=bmp)

        sizer1.Add(img_ctrl, 0, wx.ALL, 5)

    panel2.SetSizer(sizer1)
    panel2.FitInside()
    panel2.Layout()# because we are adding one by one 

    
def count_red_pixels_button(event):
    if not paths:
        print("No images selected!")
        return None
    countRedPixels.count_pixels(paths,panel2)

def detect_object_button(event):
    if not paths:
        print("No images selected!")
        return None
    detectObjects.detect_object(paths)

def dominant_colour_button(event):
    if not paths:
        print("No image is selected!")
        return None
    detectDominantColour.dominant_colour(paths,panel2)

def histogram_button(event):
    global image_paths_for_hist,panel3
    paths_histo = []
    path1 = image_paths_for_hist.get("image1")
    path2 = image_paths_for_hist.get("image2")
    paths_histo.append(path1) 
    paths_histo.append(path2) 
    if not path1 or not path2:
        print("Please load both Image 1 and Image 2!")
        return None
    histogram.histogram_difference(paths_histo, panel3)

def load_image(event):
    
    if event.GetEventObject() == btn7:
        key = "image1"
    elif event.GetEventObject() == btn8:
        key = "image2"
    else:
        return

    wildcard = "Image files(.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    choose_window = wx.FileDialog(None, f"Select {key}", wildcard=wildcard, style=wx.FD_OPEN)
    
    path = None
    if choose_window.ShowModal() == wx.ID_OK:
        path = choose_window.GetPath()
    choose_window.Destroy()

    if path:
        global image_paths_for_hist
        image_paths_for_hist[key] = path

        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
        
        img = img.Scale(300, 200)
        bmp = wx.Bitmap(img)
    
        img_ctrl = image_controls_for_hist[key]
        img_ctrl.SetBitmap(bmp)

        panel3.Layout()
   


app1 = wx.App()
frame1 = wx.Frame(None, title = "Image Processing and Analysis Toolkit", size = (1500,900))
panel1 = wx.Panel(frame1)
panel1.SetBackgroundColour("#F5EEFF")


panel2 = wx.ScrolledWindow(frame1, style=wx.VSCROLL )
panel2.SetScrollRate(20, 20)
panel2.SetBackgroundColour("#9AE3F0")

panel3 = wx.Panel(frame1)
panel3.SetBackgroundColour("#C3F98AFF")

sizer = wx.BoxSizer(wx.HORIZONTAL)
sizer.Add(panel1, 1, wx.EXPAND | wx.ALL, 0)
sizer.Add(panel2, 3, wx.EXPAND | wx.ALL, 0)
sizer.Add(panel3, 2, wx.EXPAND | wx.ALL, 0)

frame1.SetSizer(sizer)

btn1 = wx.Button(panel1,label = "Select image")
btn2 = wx.Button(panel1,label = "Convert to \n GreyScale")
btn3 = wx.Button(panel1,label = "Count Number of \n Red Pixels")
btn5 = wx.Button(panel1,label = "Detect the \n dominant colour")
btn4 = wx.Button(panel1,label = "Detect Objects")
btn6 = wx.Button(panel3,label = "Histogram difference")
text = wx.StaticText(panel1,label = "Pixel Toolkit")
btn7 = wx.Button(panel3,label = "Load image 1")
btn8 = wx.Button(panel3,label = "Load image 2")

font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
# btn1.SetBackgroundColour(wx.Colour("#E37CDC"))
btn1.SetFont(font)
btn2.SetFont(font)
btn3.SetFont(font)
btn4.SetFont(font)
btn5.SetFont(font)
btn6.SetFont(font)
btn7.SetFont(font)
btn8.SetFont(font)

font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
text.SetForegroundColour(wx.Colour("#520883"))
text.SetFont(font)


btn1.Bind(wx.EVT_BUTTON, choose_image)
btn2.Bind(wx.EVT_BUTTON, to_greyscale)
btn3.Bind(wx.EVT_BUTTON, count_red_pixels_button)
btn5.Bind(wx.EVT_BUTTON, dominant_colour_button)
btn4.Bind(wx.EVT_BUTTON, detect_object_button)
btn6.Bind(wx.EVT_BUTTON, histogram_button)
btn7.Bind(wx.EVT_BUTTON, load_image)
btn8.Bind(wx.EVT_BUTTON, load_image)


sizer4=wx.GridSizer(7,1,50,50)
# sizer =wx.BoxSizer(wx.VERTICAL)
sizer4.Add(text, 1,wx.ALIGN_CENTER | wx.ALL,5)
sizer4.Add(btn1, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn2, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn3, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn5, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn4, 1,wx.EXPAND | wx.ALL,5)


sizer5 = wx.GridSizer(3, 2, 20, 20)#the sizer for the images/buttons
sizer5.Add(btn7, 1, wx.ALL, 10)#load image 1 button
sizer5.Add(btn8, 1, wx.ALL, 10)#load image 2 button


img_ctrl1 = wx.StaticBitmap(panel3, bitmap=wx.NullBitmap)
img_ctrl2 = wx.StaticBitmap(panel3, bitmap=wx.NullBitmap)

sizer5.Add(img_ctrl1, 1, wx.ALL | wx.EXPAND, 3)
sizer5.Add(img_ctrl2, 1, wx.ALL | wx.EXPAND, 3)

sizer3 = wx.BoxSizer(wx.VERTICAL) 
sizer3.Add(btn6, 0, wx.ALL | wx.EXPAND, 10) 
sizer3.Add(sizer5, 1, wx.EXPAND | wx.ALL, 10) 

panel3.SetSizer(sizer3)


image_paths_for_hist = {"image1": None, "image2": None}
image_controls_for_hist = {"image1": img_ctrl1, "image2": img_ctrl2}

panel1.SetSizer(sizer4)

frame1.Show() 
app1.MainLoop()