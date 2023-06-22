import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image
from skimage import exposure
from skimage import measure
from skimage.color import rgb2gray
from skimage.util import compare_images

#img1 = image.imread('black_white_empty.png')
#img2 = image.imread('black_white_2.png')
#img2 = image.imread('black_white_1.png')
img1 = image.imread('img0.png')
for i in range(9, 1, -1):
    img2 = image.imread('img{}.png'.format(i))

    diff_rotated = compare_images(img1, img2, method='diff')

    mask = diff_rotated > 0

    image_gray = rgb2gray(diff_rotated)
    #image_gray = exposure.adjust_log(image_gray, 1.5) # збільшуємо яскравість
    contours = measure.find_contours(image_gray, 0.01)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img2, cmap=plt.cm.gray)
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    ax.plot()
    ax.axis('image')
    plt.tight_layout()
    plt.show()
