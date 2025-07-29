#!/usr/bin/env python3
"""
Full-Lifecycle Overseer for ChatGPT Agent Mode
Monitors a Chrome instance running under remote-debugging on port 9222
and automatically:
1. Clicks any “Retry” button that appears after a server timeout
2. Replies “confirm” when the agent asks for confirmation
"""

import time
import os
import shlex
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# ---------- Helper: send "confirm" to the ChatGPT prompt box ----------
def send_chatgpt_confirm(driver, timeout=5):
    """
    Detects any agent confirmation prompt and replies 'confirm'.
    Returns True if the reply was sent, False otherwise.
    """
    try:
        # 1. Wait for the prompt text in the *last* assistant message
        assistant_selector = "[data-message-author-role='assistant']"
        WebDriverWait(driver, timeout).until(
            lambda d: any(
                ("Ready to submit" in el.text or 'Just say "confirm"' in el.text)
                for el in d.find_elements(By.CSS_SELECTOR, assistant_selector)
            )
        )

        # 2. Locate the prompt-textarea (inside a Shadow DOM)
        main = driver.find_element(By.TAG_NAME, "main")
        shadow_root = driver.execute_script("return arguments[0].shadowRoot", main)
        textarea = shadow_root.find_element(By.CSS_SELECTOR, "textarea#prompt-textarea")

        # 3. Type "confirm" and hit Enter
        textarea.send_keys("confirm")
        textarea.send_keys(Keys.RETURN)
        return True

    except TimeoutException:
        return False
    except Exception as e:
        print("WARN: Could not send confirm:", e)
        return False


# ---------- Main loop ----------
if __name__ == "__main__":
    print("Starting Full-Lifecycle Overseer for ChatGPT Agent...")

    # Connect to the existing Chrome instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"\nFATAL ERROR: Could not connect. Is Chrome running with --remote-debugging-port=9222 ? {e}")
        exit()

    print("\n" + "=" * 60)
    print("Successfully attached. Monitoring all states.")
    print("Press Ctrl-C to stop.")
    print("=" * 60 + "\n")

    # XPath for the platform-level "Retry" button
    RETRY_BTN_XPATH = "//button[normalize-space()='Retry']"

    while True:
        try:
            driver.switch_to.default_content()

            # 1. Handle server-timeout "Retry" button
            try:
                retry_btn = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, RETRY_BTN_XPATH))
                )
                print("WARN: Platform disconnect detected! Clicking 'Retry'...")
                retry_btn.click()
                print("--> Connection re-established.")
                time.sleep(5)
                continue
            except TimeoutException:
                pass

            # 2. Handle agent confirmation prompts
            if send_chatgpt_confirm(driver):
                print("SUCCESS: Confirmation sent.")
                time.sleep(8)  # Let the agent process
                continue

        except KeyboardInterrupt:
            print("\nScript stopped by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error in main loop: {e}")
            time.sleep(3)

        # Small idle delay to keep CPU usage low
        time.sleep(2)

    print("Script finished.")
