#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import numpy
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]


def goPreviousApp():
    start_coor = ("390 ", "2381 ")
    end_coor = ("1052 ", "2381 ")
    device.shell("input touchscreen swipe " +
                 start_coor[0] + start_coor[1] + end_coor[0] + end_coor[1]+"250")


def goNextApp():
    start_coor = ("686 ", "2381 ")
    end_coor = ("200 ", "2381 ")
    device.shell("input touchscreen swipe " +
                 start_coor[0] + start_coor[1] + end_coor[0] + end_coor[1]+"250")


def cropImg(img, box):
    xstart, ystart, xend, yend = box
    return img[ystart:yend, xstart:xend, :]


def startApp():
    # Home
    device.shell("input keyevent 3")
    time.sleep(0.5)
    # Tab Page 2
    device.shell("input swipe 520 2050 520 2050 250")
    time.sleep(0.5)
    # Tab Shopee Html Pick Code
    device.shell("input swipe 664 1828 664 1828 250")
    time.sleep(0.5)
    # Home
    device.shell("input keyevent 3")
    time.sleep(0.5)
    # Tab Shopee App
    device.shell("input swipe 156 1204 156 1204 250")
    goPreviousApp()
    image = device.screencap()


image = device.screencap()
startApp()
image_filename = "screen.png"
with open(image_filename, 'wb') as f:
    f.write(image)

image = Image.open('screen.png')
imageBi = image.convert('LA')
box = (100, 100, 400, 400)
print(imageBi.format, imageBi.size, imageBi.mode)
image = numpy.array(image, dtype=numpy.uint8)
# (2400, 1080, 4) image.shape
image = image[:, :, :3]
# imageBi.save('greyscale.png')
# r , g ,b = image
# image = cropImg(image, box)
# print(image.shape)
# for index, pixel in enumerate(image[30]):
#     r, g, b = [int(i) for i in pixel]
#     print(r, g, b)
# new_im = Image.fromarray(image)
# new_im.save("numpy_screenshot.jpg")
