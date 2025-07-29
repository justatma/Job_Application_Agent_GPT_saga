#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome = Options()
chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome)

print("🔍 scanning page …")
# wait until the prompt text appears
try:
    WebDriverWait(driver, 3).until(
        lambda d: "Would you like me to click" in d.page_source
    )
    print("✅ prompt text found")
except:
    print("❌ prompt text NOT found")
    driver.quit()
    exit()

# try to locate the editable box
try:
    box = driver.find_element(By.ID, "prompt-textarea")
    print("✅ prompt-textarea div found")
    box.clear()
    box.send_keys("yes")
    box.send_keys(Keys.RETURN)
    print("✅ typed 'yes' + Enter")
except Exception as e:
    print("❌ error or box not found:", e)

time.sleep(1)
driver.quit()
