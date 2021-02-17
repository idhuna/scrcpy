import pyautogui
from time import sleep
import keyboard

print('Press Ctrl-C to quit.')
shortcut = 'a'  # define your hot-key
print('Hotkey set as:', shortcut)


def start():  # define your function to be executed on hot-key press
    print('Running')
    while True:
        # if(pyautogui.locateOnScreen('partialCode.png', region=(video['left'],video['top'], video['width'], video['height']), grayscale=True, confidence=0.9)):
        #     text = getText()
        #     text = correctText(text)
        #     if(text):
        #         pyautogui.typewrite(text)
        #         pyperclip.copy(text)
        #         break
        # else:
        #     print('Not Found')
        #     sleep(3)
        currentMouseX, currentMouseY = pyautogui.position()
        print(currentMouseX, currentMouseY)
        # pyautogui.click(1000, 888)
        print(pyautogui.size())
        im = pyautogui.screenshot('foo.png')
        print("im", im.getpixel((598*2, 319*2)))
        pix = pyautogui.pixel(598*2, 319*2)
        print(pix)
        # pyautogui.scroll(-10)
        # print(pyautogui.position())
        # pyautogui.alert('This is the message to display.')
        sleep(5)


keyboard.add_hotkey(shortcut, start)  # <-- attach the function to hot-key

print("Press ESC to stop.")
try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print('\nDone.')
