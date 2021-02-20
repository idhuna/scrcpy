import pyautogui
import numpy as np
# 789, 1622
ss = pyautogui.screenshot('ss.png', region=(92, 160, 697, 1462))
while(True):
    print(pyautogui.pixel(*pyautogui.position()))
