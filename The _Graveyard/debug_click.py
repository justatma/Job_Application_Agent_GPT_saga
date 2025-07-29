#!/usr/bin/env python3
import time, requests, json, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = webdriver.ChromeOptions()
opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(), options=opts)

print("🔍 Looking for Confirm button …")
while True:
    try:
        btn = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, 
"//button[text()='Confirm']"))
        )
        print("✅ Found & clicking now!")
        btn.click()
        break
    except:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.5)
