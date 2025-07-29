#!/usr/bin/env python3
"""
agent_overseer.py
Watches the new ChatGPT Agent Mode and injects “yes” when asked to confirm.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------


def send_agent_yes(driver):
    """Send 'yes' to the Agent prompt box."""
    try:
        # 1. Wait until the prompt text appears
        WebDriverWait(driver, 4).until(
            lambda d: "Would you like me to click" in d.page_source
        )

        # 2. Grab the content-editable div
        box = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "prompt-textarea"))
        )

        # 3. Clear placeholder, type 'yes', hit Enter
        box.clear()
        box.send_keys("yes")
        box.send_keys(Keys.RETURN)
        print("✅ Sent 'yes' + Enter")
        return True
    except TimeoutException:
        return False
# ------------------------------------------------------------
if __name__ == "__main__":
    print("Starting Agent-Mode Overseer…")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Attached to Agent tab. Press Ctrl-C to stop.")

    retry_xpath = "//button[normalize-space()='Retry']"

    while True:
        try:
            driver.switch_to.default_content()

            # 1. Handle server-timeout Retry
            try:
                retry_btn = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, retry_xpath))
                )
                retry_btn.click()
                print("Clicked Retry")
                time.sleep(5)
                continue
            except TimeoutException:
                pass

            # 2. Confirm submission
            if send_agent_yes(driver):
                print("Confirmation sent")
                time.sleep(8)
                continue

        except KeyboardInterrupt:
            print("\nStopping.")
            break
        except Exception as e:
            print(f"Unexpected: {e}")
            time.sleep(3)

        time.sleep(2)

