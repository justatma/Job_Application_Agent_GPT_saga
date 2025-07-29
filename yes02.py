#!/usr/bin/env python3
"""
yes02.py - Types 'yes' every 5 minutes
"""
import time
import pyautogui

print("Will type 'yes' every 5 minutes...")
print("Keep ChatGPT tab active!")

while True:
    time.sleep(300)  # 5 minutes
    
    print(f"Typing 'yes' at {time.strftime('%H:%M:%S')}")
    pyautogui.typewrite('yes')
    pyautogui.press('enter')
 
