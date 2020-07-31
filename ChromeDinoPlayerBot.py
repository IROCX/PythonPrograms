
# A simple python script for computer to play Google Chrome's Dino as CPU Bot

import pyautogui
from PIL import Image, ImageGrab
import time

def takeScreenshot():
    return ImageGrab.grab().convert('L')

def isCollide(data):
    for i in range(480,510):
        for j in range(680,690):
            if data[i, j] < 100:
                pyautogui.keyUp('down')
                pyautogui.keyDown('up')
                return
    for i in range(480,510):
        for j in range(560,570):
            if data[i, j] < 100:
                pyautogui.keyUp('up')
                pyautogui.keyDown('down')
                return
    
    return


print("Starting... in 3 secs")
time.sleep(3)
while True:
    data = takeScreenshot().load()
    isCollide(data)


# un-comment this code and comment out while loop above to view the detecting rectangle regions

# image = takeScreenshot()
# data = image.load()
# for i in range(400,410):
#         for j in range(680,690):
#             data[i, j] = 0
# for i in range(400,410):
#         for j in range(550,560):
#             data[i, j] = 0
    
# image.show()