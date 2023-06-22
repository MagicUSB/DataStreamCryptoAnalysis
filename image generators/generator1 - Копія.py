from PIL import Image, ImageDraw

width = 500
height = 500
rect_width = width - 200
cnt = 1
shape = [(100, 100), (rect_width, rect_width)]
img  = Image.new( mode = "RGB", size = (width, height), color = (255, 255, 255) )
img1 = ImageDraw.Draw(img)
img.save("img_1_0.png")
while rect_width > 100:
    shape = [(100, 100), (rect_width, rect_width)]
    img  = Image.new( mode = "RGB", size = (width, height), color = (255, 255, 255) )
    img1 = ImageDraw.Draw(img)  
    img1.rectangle(shape, fill=(255, 255, 0), outline ="yellow")
    #img.show()
    img.save("img_1_{}.png".format(cnt))
    cnt += 1
    rect_width -=50
    print(rect_width)
    shape = [(0, 0), (rect_width, rect_width)]