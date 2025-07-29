
# The Graveyard of Good Intentions  
*A Chronological History of Failed Scripts*

This document provides a **BRIEF chronological history** of every major script developed in an attempt to automate the OpenAI Operator and ChatGPT Agent.  
(Note that there were nearly 70 attempted scripts in the saga.)

Each of the approaches below represents a logical, well-reasoned—and ultimately flawed—approach to the problem.  
They serve as a testament to the challenges of automating complex, dynamic, and protected web applications.

---

## Attempt 1: The All-in-One Automator (Selenium)  
***(Circa: The Legacy "Operator" Era)***

### **Hypothesis:**  
The initial assumption was that our script needed to be both the *"brains"* and the *"finger"*.  
This monolithic script was designed to not only click the final "Submit" button but also to answer questions from a built-in `ANSWER_BANK`, duplicating logic that the agent was already handling.

### **Generated Python**
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

--- Configuration ---
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
STARTING_URL = "https://www.linkedin.com/jobs/search/?f_AL=true&keywords=python%20developer"

--- Your Answer Bank ---
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

--- Main Automation Script ---
if name == "main":
# ... (Setup code for Selenium to launch a new browser)

text
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
            submit_button_xpath = "//button[@aria-label and \
                (contains(., 'Submit') or contains(., 'Review') or contains(., 'Next'))]"
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
text

### **Outcome:**  
**Failed.** This approach was overly complex and based on the incorrect assumption that the Operator view was a simple webpage.

---

## Attempt 2: The Focused "Overseer" — The Descent into DOM Complexity  
***(Circa: The New "ChatGPT Agent" Era)***

### **Hypothesis:**  
With the new Agent Mode, the problem was simplified: just handle the confirmation.  
It was believed the prompt was inside a complex structure of **iframes** and **Shadow DOMs**.  
This script was the first attempt to navigate this supposed structure and handle the platform's *"Retry"* button.

### **Generated Python**
#!/usr/bin/env python3
"""
overseer.py
Watches the Operator browser tab and:

Clicks "Retry" errors

Sends “confirm” when Operator asks
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
prompt_selector = "[data-message-author-role='assistant']"
WebDriverWait(driver, 3).until(
lambda d: any(
"Ready to submit" in el.text for el in d.find_elements(By.CSS_SELECTOR, prompt_selector)
)
)
# Assumes input is in a shadow-root
main = driver.find_element(By.TAG_NAME, "main")
shadow = driver.execute_script("return arguments.shadowRoot", main)
textarea = shadow.find_element(By.CSS_SELECTOR, "textarea#prompt-textarea")
textarea.send_keys("confirm")
textarea.send_keys(Keys.RETURN)
return True
except TimeoutException:
return False

def main():
retry_xpath = "//button[normalize-space()='Retry']"
while True:
try:
driver.switch_to.default_content()
try:
retry_btn = WebDriverWait(driver, 1).until(
EC.element_to_be_clickable((By.XPATH, retry_xpath))
)
retry_btn.click()
time.sleep(5)
continue
except TimeoutException:
pass
if send_operator_confirm(driver):
print("Sent 'confirm'")
time.sleep(10)
continue
except KeyboardInterrupt:
break
except Exception as e:
time.sleep(3)

text
print("Script finished.")
if name == "main":
main()

text

### **Outcome:**  
**Failed.** The script could not find the prompt text or textarea, proving the **iframe / Shadow DOM** theory was likely incorrect.

---

## Diagnostic Tool 1: The "Are We Crazy?" Minimalist Test  
***(Circa: The “Why can’t Selenium see anything?” Phase)***

### **Hypothesis:**  
Could Selenium see the prompt text or the *Confirm* button **anywhere** in the visible DOM?

### **Generated Python**
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

print("🔍 scanning page …")

Test 1: Wait until prompt text appears
try:
WebDriverWait(driver, 3).until(
lambda d: "Would you like me to click" in d.page_source
)
print("✅ prompt text found in page source")
except:
print("❌ prompt text NOT found in page source")
driver.quit()
exit()

Test 2: Locate editable box by ID
try:
box = driver.find_element(By.ID, "prompt-textarea")
print("✅ prompt-textarea div found")
box.send_keys("yes", Keys.RETURN)
print("✅ typed 'yes' + Enter")
except Exception as e:
print("❌ error or box not found:", e)

driver.quit()

text

### **Outcome:**  
**Failed.** The script printed: `❌ prompt text NOT found` — confirming the Agent’s prompt was not in the accessible HTML.

---

## Attempt 3: The Visual Automator — The Pivot to `pyautogui`  
***(Circa: The “Let’s look at the screen” Phase)***

### **Hypothesis:**  
If Selenium can't read the DOM, the UI must be a canvas or streamed as graphics.  
The solution: use `pyautogui` to visually scan and click based on image recognition.

### **Generated Python**
import time
import pyautogui
from selenium import webdriver # Still used for Retry handling

--- Configuration ---
CONFIRM_BUTTON_DAY_IMAGE = 'confirm_button_day.png'
CONFIRM_BUTTON_NIGHT_IMAGE = 'confirm_button_night.png'
RETRY_BUTTON_XPATH = "//button[normalize-space()='Retry']"

if name == "main":
while True:
try:
# --- Priority 1: Look for Confirm button ---
button_location = None
try:
button_location = pyautogui.locateOnScreen(
CONFIRM_BUTTON_DAY_IMAGE, grayscale=True, confidence=0.8
)
if button_location is None:
button_location = pyautogui.locateOnScreen(
CONFIRM_BUTTON_NIGHT_IMAGE, grayscale=True, confidence=0.8
)
except pyautogui.PyAutoGUIException:
pass

text
        if button_location:
            print("SUCCESS: Confirm button found, clicking.")
            pyautogui.click(pyautogui.center(button_location))
            time.sleep(5)
            continue

        # --- Priority 2: Retry logic (via Selenium) ---
        # ... omitted for brevity ...

    except KeyboardInterrupt:
        break
    except Exception as e:
        time.sleep(3)

    time.sleep(2)
text

### **Outcome:**  
**Failed.** After navigating macOS's accessibility permissions, the script still couldn’t interact. Synthetic clicks were dropped—suggesting OS-level protection against simulated device events.

---

## ✅ The Solution: *The Peterkin Protocol* — A 9-Line Timed Keyboard Typer  
***(Circa: The “Stop Being Smart” Epiphany)***

### **Hypothesis:**  
Stop trying to "detect" anything.  
Let the Agent stop when it needs confirmation—and **just simulate typing** with a delay.  
No DOM. No screenshot. No sensors. Just **keys** on a timer.

### **Final Winning Script**
#!/usr/bin/env python3
"""
yes02.py - Types 'yes' every 5 minutes
"""
import time
import pyautogui

print("Will type 'yes' every 5 minutes...")
print("Keep ChatGPT tab active!")

while True:
time.sleep(300) # 5 minutes
print(f"Typing 'yes' at {time.strftime('%H:%M:%S')}")
pyautogui.typewrite('yes')
pyautogui.press('enter')

text

**[HAHAHAHA…](pplx://action/followup)**  
> After 60+ failed scripts, three world-leading AIs, and every tool in the Python automation toolbox…  
> The final solution was a timer and a keyboard emulator.
