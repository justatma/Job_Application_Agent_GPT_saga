# The Graveyard of Good Intentions: 

A Chronological History of Failed Scripts

This document provides a BRIEF chronological history of every major script developed in an attempt to automate the OpenAI Operator and ChatGPT Agent. (Note that there were nearly 70 attempted scripts in the saga) Each of the approaches below represents a logical, well-reasoned—and ultimately flawed approach to the problem. They serve as a testament to the challenges of automating complex, dynamic, and protected web applications.

### Attempt 1: The All-in-One Automator (Selenium)

*(Circa: The Legacy "Operator" Era)*

**Hypothesis:** The initial assumption was that our script needed to be both the "brains" and the "finger." This monolithic script was designed to not only click the final "Submit" button but also to answer questions from a built-in ANSWER_BANK, duplicating logic that the agent was already handling.

#### Generated python

```python
import time
import os
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
STARTING_URL = "https://www.linkedin.com/jobs/search/?f_AL=true&keywords=python%20developer"

# --- Your Answer Bank ---
ANSWER_BANK = {
    "how many years of experience do you have with python": "5",
    "what is your desired salary": "120000",
    "are you legally authorized to work in the united states": "Yes",
    "will you now or in the future require sponsorship": "No",
}

def get_answer_for_question(question_text):
    # ... (Function to search the answer bank)
    return None

def human_like_delay(min_seconds=0.5, max_seconds=1.5):
    time.sleep(random.uniform(min_seconds, max_seconds))

# --- Main Automation Script ---
if __name__ == "__main__":
    # ... (Setup code for Selenium to launch a new browser)
    
    # --- Step 1: Manual Login ---
    # ... (Code to wait for the user to log in)
    
    # --- Step 2: Main Application Loop ---
    while True:
        try:
            # --- Step 3: Detect and Handle the "Easy Apply" Modal ---
            modal_xpath = "//div[contains(@class, 'jobs-easy-apply-modal')]"
            modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, modal_xpath))
            )
            
            while True:
                # --- Step 4: Answer Questions on the Page ---
                # ... (Complex logic to find questions and populate answers)
                
                # --- Step 5: Find and Click the Next/Review/Submit Button ---
                submit_button_xpath = "//button[@aria-label and (contains(., 'Submit') or contains(., 'Review') or contains(., 'Next'))]"
                submit_button = modal.find_element(By.XPATH, submit_button_xpath)
                
                if "submit application" in submit_button.text.lower():
                    print("SUCCESS: Found 'Submit Application' button. Clicking now!")
                    submit_button.click()
                    break
                else:
                    submit_button.click()
                    
        except TimeoutException:
            pass
        except Exception as e:
            break
    
    driver.quit()
```

**Outcome:** Failed. This approach was overly complex and based on the incorrect assumption that the Operator view was a simple webpage.

### Attempt 2: The Focused "Overseer" - The Descent into DOM Complexity

*(Circa: The New "ChatGPT Agent" Era)*

**Hypothesis:** With the new Agent Mode, the problem was simplified: just handle the confirmation. Based on initial analysis, it was believed the prompt was inside a complex structure of iframes and Shadow DOMs. This script was the first attempt to navigate this supposed structure and also introduced the logic for handling the platform's "Retry" button.

#### Generated python

```python
#!/usr/bin/env python3
"""
overseer.py
Watches the Operator browser tab and:
  - Clicks "Retry" errors
  - Sends "confirm" when Operator asks
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

def send_operator_confirm(driver):
    try:
        # Tries to find the prompt in the last message
        prompt_selector = "[data-message-author-role='assistant']"
        WebDriverWait(driver, 3).until(
            lambda d: any(
                "Ready to submit" in el.text for el in d.find_elements(By.CSS_SELECTOR, prompt_selector)
            )
        )
        
        # Assumes input is in a shadow-root
        main = driver.find_element(By.TAG_NAME, "main")
        shadow = driver.execute_script("return arguments[0].shadowRoot", main)
        textarea = shadow.find_element(By.CSS_SELECTOR, "textarea#prompt-textarea")
        
        textarea.send_keys("confirm")
        textarea.send_keys(Keys.RETURN)
        return True
    except TimeoutException:
        return False

def main():
    # ... (Main loop to connect to Chrome on port 9222)
    retry_xpath = "//button[normalize-space()='Retry']"
    
    while True:
        try:
            driver.switch_to.default_content()
            
            # 1. Handle Retry button
            try:
                retry_btn = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, retry_xpath)))
                retry_btn.click()
                time.sleep(5)
                continue
            except TimeoutException:
                pass
            
            # 2. Handle confirmation
            if send_operator_confirm(driver):
                print("Sent 'confirm'")
                time.sleep(10)
                continue
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(3)
    
    print("Script finished.")

if __name__ == "__main__":
    main()
```

**Outcome:** Failed. The script could not find the prompt text or the textarea, proving the iframe / Shadow DOM theory was likely incorrect.

### Diagnostic Tool 1: The "Are We Crazy?" Minimalist Test

*(Circa: The "Why can't Selenium see anything?" Phase)*

**Hypothesis:** After repeated failures, we needed to prove a basic fact: could Selenium see the prompt text or the Confirm button *anywhere* in the accessible DOM? This script was a minimal, brute-force test.

#### Generated python

```python
#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome = Options()
chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome)

print("🔍 scanning page ...")

# Test 1: Wait until the prompt text appears anywhere in the raw page source
try:
    WebDriverWait(driver, 3).until(
        lambda d: "Would you like me to click" in d.page_source
    )
    print("✅ prompt text found in page source")
except:
    print("❌ prompt text NOT found in page source")
    driver.quit()
    exit()

# Test 2: Try to locate the editable box by its ID
try:
    box = driver.find_element(By.ID, "prompt-textarea")
    print("✅ prompt-textarea div found")
    box.send_keys("yes", Keys.RETURN)
    print("✅ typed 'yes' + Enter")
except Exception as e:
    print("❌ error or box not found:", e)

driver.quit()
```

**Outcome:** Failed. The script printed ❌ prompt text NOT found, proving definitively that the agent's prompt was not present in the main HTML document that Selenium could access.

### Attempt 3: The Visual Automator - The Pivot to pyautogui

*(Circa: The "Let's look at the screen" Phase)*

**Hypothesis:** If Selenium can't read the DOM, the UI must be a video stream or a \<canvas\> element. The only way to interact is to abandon the DOM and use visual recognition to find an image of the button on the screen.

#### Generated python

```python
import time
import pyautogui
from selenium import webdriver  # Still needed for the Retry button

# --- Configuration ---
CONFIRM_BUTTON_DAY_IMAGE = 'confirm_button_day.png'
CONFIRM_BUTTON_NIGHT_IMAGE = 'confirm_button_night.png'
RETRY_BUTTON_XPATH = "//button[normalize-space()='Retry']"

if __name__ == "__main__":
    # ... (Connect to Chrome)
    
    while True:
        try:
            # --- Priority 1: Visually find the Confirm button (Day or Night) ---
            button_location = None
            
            try:
                # Look for day/night mode buttons using tolerant, grayscale matching
                button_location = pyautogui.locateOnScreen(
                    CONFIRM_BUTTON_DAY_IMAGE,
                    grayscale=True,
                    confidence=0.8
                )
                if button_location is None:
                    button_location = pyautogui.locateOnScreen(
                        CONFIRM_BUTTON_NIGHT_IMAGE,
                        grayscale=True,
                        confidence=0.8
                    )
            except pyautogui.PyAutoGUIException:
                pass
            
            if button_location:
                print("SUCCESS: Visual 'Confirm' button found! Clicking now.")
                pyautogui.click(pyautogui.center(button_location))
                time.sleep(5)
                continue
            
            # --- Priority 2: Handle Selenium 'Retry' button ---
            try:
                # ... (Logic to find and click the Retry button)
                pass
            except:
                pass
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(3)
        
        time.sleep(2)
```

**Outcome:** Failed. After a long and arduous battle with macOS permissions (Screen Recording, Accessibility, Input Monitoring), the script was finally able to run but still could not find the image on screen or, when given coordinates, the click would not register. This proved a deep-level system block was in place against synthetic mouse events.

### The Solution: The Peterkin Protocol - A 9-Line Timed Keyboard Typer

*(Circa: The "Stop Being Smart" Epiphany)*

**Hypothesis:** The final, user-devised solution was to abandon all forms of detection. The script doesn't need to see or know anything. It only needs to know that eventually, the agent will be waiting for input with the text box focused. By simply simulating keyboard input on a timer, it bypasses every single technical roadblock we encountered.

#### Generated python

```python
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
```

**HAHAHAHA....**