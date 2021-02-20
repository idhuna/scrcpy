#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import numpy as np
import time
import pyautogui
import cv2
from io import BytesIO

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

redColor = (0, 0, 255)
greenColor = (0, 255, 0)
shopeeColor = (238, 77, 45)
xcrop = 0
ycrop = 0


class PixelColor:

    def __init__(self, imgFilename="screen.png"):
        self.name = imgFilename
        imgBGR = cv2.imread(imgFilename)
        # imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
        self.imgBGR = imgBGR
        self.shape = imgBGR.shape
        self.coor = None

    def pixelMatchesColor(self, x, y, expectedRGBColor, tolerance=0):
        b, g, r = self.imgBGR[y, x]
        print(r, g, b)
        exR, exG, exB = expectedRGBColor
        if((abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance)):
            self.coor = (x, y)
            return True


def clickOnDevice(x, y):
    if(x == 0 and y == 0):
        return
    print("input swipe {:.0f} {:.0f} {:.0f} {:.0f} 250".format(x, y, x, y))
    device.shell(
        "input swipe {:.0f} {:.0f} {:.0f} {:.0f} 250".format(x, y, x, y))


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
    global xcrop
    global ycrop
    xcrop = xstart
    ycrop = ystart
    return img[ystart:yend, xstart:xend]


def refreshScreencap(imgFilename="screen.png"):
    image = device.screencap()
    with open(imgFilename, 'wb') as f:
        f.write(image)


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
    input("Please select items then Press Enter to continue...")
    goPreviousApp()
    time.sleep(0.5)
    device.shell("input swipe 600 950 600 950 250")
    image = device.screencap()


def findByTemplate(imgFilename, templateFilename, box=False, threshold=0.999, findIndex=-1):  # -1 is Find All
    imgBGR = cv2.imread(imgFilename)
    if(box):
        cropImgBGR = cropImg(imgBGR, box)
        imgGrey = cv2.cvtColor(cropImgBGR, cv2.COLOR_BGR2GRAY)
    else:
        global xcrop
        global ycrop
        xcrop = 0
        ycrop = 0
        imgGrey = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('res1.png', cropImgBGR)
    template = cv2.imread(templateFilename, 0)
    w, h = template.shape[::-1]
    # Print w,h
    # print(w, h)
    # TM_CCOEFF TM_CCOEFF_NORMED TM_CCORR_NORMED TM_SQDIFF (MIN)
    res = cv2.matchTemplate(imgGrey, template, cv2.TM_CCOEFF_NORMED)
    if(findIndex):
        loc = np.where(res >= threshold)
    else:
        loc = np.where((res == np.max(res)) & (res >= threshold))
    y = 0
    coorAllOnImg = []
    if(len(loc[0]) > 0):
        for index, pt in enumerate(zip(*loc[::-1])):
            if(findIndex > 0 and index != (findIndex-1)):
                continue
            dy = abs(pt[1] + h//2 - y)
            y = pt[1] + h//2
            xcoor = xcrop + pt[0]
            ycoor = ycrop + pt[1]
            if(y <= 100 or dy > 100):
                coorAllOnImg.append((xcoor + w//2, ycoor + h//2))
                cv2.rectangle(imgBGR, (xcoor, ycoor),
                              (xcoor + w, ycoor + h), redColor, 2)
                cv2.circle(imgBGR, (xcoor + w//2, ycoor + h//2),
                           10, greenColor, 10)
            if(findIndex == 0):
                return coorAllOnImg
        # BGR color space
        cv2.imwrite('res.png', imgBGR)
    else:
        # print("Template Matching Not Found! Max is :", np.max(res))
        return None
    return coorAllOnImg


def clickCodeThenBuy():
    while True:
        # refesh
        device.shell("input swipe 540 180 540 900 150")
        while(PixelColor().pixelMatchesColor(276, 2022, shopeeColor, 1)):
            start2 = time.time()
            refreshScreencap()
            end2 = time.time()
            print(end2 - start2)
        print('imba')
        # swipe up
        # device.shell("input swipe 540 1440 540 600 500")
        while(not PixelColor().pixelMatchesColor(276, 2022, shopeeColor, 0)):
            refreshScreencap()
        box = (806, 451, 1022, 2106)
        pickCode = findByTemplate(
            image_filename, "pickCode.png", box, 0.95, findIndex=0)
        if(pickCode):
            clickOnDevice(*pickCode[0])
            break
    time.sleep(0.25)
    goPreviousApp()
    indexShopeeColor = [(285, 1439), (285, 200)]
    # goto page choose code
    chooseCodes = [(872, 1528), (872, 1310)]
    refreshScreencap()
    while(not PixelColor().pixelMatchesColor(*indexShopeeColor[0], shopeeColor, 1)):
        # goto page choose code
        clickOnDevice(*chooseCodes[0])
        refreshScreencap()
    indexSelectCode = [(984, 1170), (984, 1491)]
    clickOnDevice(*indexSelectCode[0])
    # select Code
    # for i in range(2):
    #     boxDiscount = (0, 1020, 1080, 2222)
    #     circleOutline = findByTemplate(
    #         image_filename, 'circle-outline.png', boxDiscount, 0.98, 0)
    #     refreshScreencap()
    #     if(circleOutline):
    #         clickOnDevice(*circleOutline[0])
    #         break
    # # ตกลง
    # # time.sleep(0.2)
    # clickOnDevice(541, 2300)
    # # ชำระเงิน
    # clickOnDevice(950, 2300)
    print("DONE")


start = time.time()
image_filename = "screen.png"
clickOnDevice(200, 300)
# refreshScreencap()
# startApp()
# clickCodeThenBuy()


boxProfile = (960, 130, 1080, 250)
test = findByTemplate(
    image_filename, 'profile.png', boxProfile, 0.98, 0)
# clickOnDevice(*test[0])
boxCheckout = (885, 590, 1050, 661)
# while True:
#     refreshScreencap()
#     test2 = findByTemplate(
#         image_filename, 'checkout.png', boxCheckout, 0.98, 0)
#     if(test2[0][0]):
#         clickOnDevice(*test2[0])
#         break
# while True:
#     refreshScreencap()
#     pix = PixelColor()
#     pix2 = pix.pixelMatchesColor(905, 2256, (238, 77, 45), 5)
#     if(pix2):
#         clickOnDevice(*pix.coor)
#         print(pix.coor)
#         break

# imgBGR = cv2.imread("screen.png")
# imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
# pixelMatchesColor(imgRGB, 420, 1598, (238, 77, 45), tolerance=0)
test = PixelColor(image_filename)
print(test.pixelMatchesColor(232, 791, (18, 122, 89), 1))
# image = numpy.array(image, dtype=numpy.uint8)
# imageBi = numpy.array(imageBi, dtype=numpy.uint8)
# (2400, 1080, 4) image.shape
# image = image[:, :, :3]
# imageBi.save('greyscale.png')
# r , g ,b = image
# image = cropImg(image, box)
# print(image.shape)
# for index, pixel in enumerate(image[30]):
#     r, g, b = [int(i) for i in pixel]
#     print(r, g, b)
# new_im = Image.fromarray(image)
# new_im.save("numpy_screenshot.jpg")

end = time.time()
print("Time used : ", end="")
print(end - start)
