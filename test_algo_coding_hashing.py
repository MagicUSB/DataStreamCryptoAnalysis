# This Python file uses the following encoding: utf-8
import hashlib

import arithmetic_encoding as ae
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image
from matplotlib.gridspec import GridSpec

from coder_methods import coder, decoder

# Послідовність дій:
# 0. Обчислюємо MD5 вихідного файлу
# 1. Завантажуємо файл і арифметично пакуємо
# 2. Додаємо хеш з бакалаврської роботи
# 3. Розкодовуємо файл і порівнюємо MD5

input_file_name = "1.jpg"
with open(input_file_name, mode="rb") as input_file:    #0
    md5_input = hashlib.md5(input_file.read()).hexdigest()
ae.encode(input_file_name, input_file_name + "_tmp.dat")    #1
arr_data = np.fromfile(input_file_name + "_tmp.dat", dtype=np.uint8)
coder.add_hash_to_message(arr_data) #2
decoder.get_message_and_errors("test.dat")
ae.decode("decoded.dat", "1_decoded.jpg")
with open("1_decoded.jpg", mode="rb") as output_file:
    md5_output = hashlib.md5(output_file.read()).hexdigest()
print("MD5 hashes of input and output are equal: {}".format(md5_input == md5_output))   #3


img = image.imread("1.jpg")
img2 = img[449:1850, 1855:3459] #вирізали частину зображення (координати (y, x))
image.imsave("1_cropped.jpg", img2)
fig = plt.figure(figsize=(8, 9))
gs = GridSpec(2, 1)
ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[1, 0])
ax0.imshow(img, cmap='gray')
ax1.imshow(img2, cmap='gray')
#plt.figure()
#plt.imshow(img2)
plt.tight_layout()
plt.show()
