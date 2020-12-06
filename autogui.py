import pyautogui
import time

pyautogui.PAUSE = 0
for i in range(1,5):
    print(i)
    time.sleep(1)

for i in range(100):
    pyautogui.click()