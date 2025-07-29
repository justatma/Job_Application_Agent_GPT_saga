#!/usr/bin/env python3
"""
retry_bot.py
A lean, single-purpose script that monitors the ChatGPT Agent tab and
automatically clicks the "Retry" button when a platform disconnect occurs.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------
if __name__ == "__main__":
    print("Starting Retry Bot for ChatGPT Agent...")
    
    # --- Connect to the existing Chrome instance ---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"\nFATAL ERROR: Could not connect. Is Chrome running with --remote-debugging-port=9222?")
        print(f"Error details: {e}")
        exit()

    print("\n" + "="*60)
    print("✅ Successfully attached to the browser.")
    print("📍 Monitoring for platform 'Retry' button...")
    print("Press Ctrl+C to stop.")
    print("="*60 + "\n")

    # The XPath for the platform-level "Retry" button
    retry_xpath = "//button[normalize-space()='Retry']"

    while True:
        try:
            # Always ensure we are looking at the main page content
            driver.switch_to.default_content()

            # Look for the "Retry" button with a short timeout
            retry_btn = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, retry_xpath))
            )
            
            # If the button is found, click it
            print("WARN: Platform disconnect detected! Clicking 'Retry'...")
            retry_btn.click()
            print("--> Connection re-established.")
            time.sleep(5) # Give the session a moment to recover

        except TimeoutException:
            # This is the normal, healthy state. The button was not found.
            pass
        except KeyboardInterrupt:
            print("\n👋 Stopping the Retry Bot.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            time.sleep(3)

        # Main polling delay to keep CPU usage low
        time.sleep(2)

    print("Script finished.")
