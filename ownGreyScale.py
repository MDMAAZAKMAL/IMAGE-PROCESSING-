from PIL import Image
grey = Image.open("image1.jpg").convert("L")
grey.show()

