import cv2
import numpy as np
import pytesseract
import pyautogui
import time
import pyperclip
import keyboard
import ocrspace

api = ocrspace.API()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Variable at twitch cinema 720p
video = {'left':376, 'top':156, 'width':2050, 'height':1153}
code = {'left':1020, 'top':310, 'width':1776-1020, 'height':402-310}

print('Press Ctrl-C to quit.')
# pyautogui.FAILSAFE = True

def showImgBGR(bgr):
    cv2.imshow('Test',bgr)
    cv2.waitKey(0)

def imgToString(img):
    # 3. Convert image to grayscale
    # img = cv2.imread('code1.png')
    image= cv2.subtract(img,np.array([50.0]))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray,(3,3),0)
    blur = cv2.medianBlur(gray, 1)
    (_, bwImg) = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
    kernel = np.ones((6,6),np.uint8)
    opening = cv2.morphologyEx(bwImg, cv2.MORPH_OPEN, kernel)
    custom_config = r'--psm 6'
    cv2.imwrite('codeImg.PNG',opening)
    showImgBGR(opening)
    # print('API',api.ocr_file('codeImg.PNG'))
    string = pytesseract.image_to_string(opening, config=custom_config)
    return string

def getText():
    im = pyautogui.screenshot(region=(code['left'],code['top'], code['width'], code['height']))
    img = np.array(im)
    # bgrImg = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    text = imgToString(img)
    print(text)
    return text.strip()

text_to_print='default_predefined_text'
shortcut = 'a' #define your hot-key
print('Hotkey set as:', shortcut)

def correctText(text):
    text = text.replace(" ", "")
    if(len(text) != 12):
        return False
    return text

def myMain(): #define your function to be executed on hot-key press
    print('Running')
    while True:
        if(pyautogui.locateOnScreen('partialCode.png', region=(video['left'],video['top'], video['width'], video['height']), grayscale=True, confidence=0.9)):
            text = getText()
            text = correctText(text)
            if(text):
                pyautogui.typewrite(text)
                pyperclip.copy(text)
                break
        else:
            print('Not Found')
            time.sleep(3)

keyboard.add_hotkey(shortcut, myMain) #<-- attach the function to hot-key

print("Press ESC to stop.")
try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print('Done.\n')


