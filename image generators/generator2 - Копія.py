from PIL import Image, ImageDraw

width = 500
height = 500
rect_width = 250
shape = [(0, 0), (rect_width, rect_width)]
img  = Image.new( mode = "RGB", size = (width, height), color = (229, 229, 229) )
img1 = ImageDraw.Draw(img)
img.save("img0.png")
for c in range(0, 256):
    img  = Image.new( mode = "RGB", size = (width, height), color = (229, 229, 229) )
    img1 = ImageDraw.Draw(img)  
    img1.rectangle(shape, fill=(c, c, c), outline = (c, c, c))
    #img.show()
    img.save("color_img{}.png".format(c))
    shape = [(0, 0), (rect_width, rect_width)]