#!/usr/bin/env python3
"""
confirm. py
Monitors ChatGPT Agent Mode and automatically confirms job submissions
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def find_and_fill_prompt_box(driver):
    """
    Finds the ChatGPT prompt box and types 'yes' + Enter
    Uses multiple strategies to ensure success
    """
    try:
        # Strategy 1: Direct ID lookup for the contenteditable div
        try:
            box = driver.find_element(By.ID, "prompt-textarea")
            if box.get_attribute("contenteditable") == "true":
                # Clear any placeholder text
                driver.execute_script("""
                    var element = arguments[0];
                    element.focus();
                    element.innerHTML = '';
                    return true;
                """, box)
                
                # Type 'yes' and send
                box.send_keys("yes")
                box.send_keys(Keys.RETURN)
                print("✅ Sent 'yes' via contenteditable div")
                return True
        except NoSuchElementException:
            pass

        # Strategy 2: Find by class name pattern
        try:
            boxes = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
            for box in boxes:
                if "ProseMirror" in box.get_attribute("class"):
                    driver.execute_script("""
                        var element = arguments[0];
                        element.focus();
                        element.innerHTML = '<p>yes</p>';
                        return true;
                    """, box)
                    
                    # Trigger input event
                    driver.execute_script("""
                        var event = new Event('input', { bubbles: true });
                        arguments[0].dispatchEvent(event);
                    """, box)
                    
                    # Send Enter key
                    box.send_keys(Keys.RETURN)
                    print("✅ Sent 'yes' via ProseMirror editor")
                    return True
        except:
            pass

        # Strategy 3: Look for any visible textarea (fallback)
        try:
            textareas = driver.find_elements(By.TAG_NAME, "textarea")
            for textarea in textareas:
                if textarea.is_displayed() and textarea.is_enabled():
                    textarea.clear()
                    textarea.send_keys("yes")
                    textarea.send_keys(Keys.RETURN)
                    print("✅ Sent 'yes' via textarea")
                    return True
        except:
            pass

        return False
    except Exception as e:
        print(f"Error in find_and_fill_prompt_box: {e}")
        return False

def monitor_for_submission_prompt(driver):
    """
    Monitors for LinkedIn job submission prompts in the agent output
    """
    last_message_count = 0
    
    while True:
        try:
            # Check for assistant messages
            assistant_messages = driver.find_elements(By.CSS_SELECTOR, 
"[data-message-author-role='assistant']")
            
            if len(assistant_messages) > last_message_count:
                # New message detected
                last_message_count = len(assistant_messages)
                
                # Get the last message text
                try:
                    last_message = assistant_messages[-1]
                    message_text = last_message.text.lower()
                    
                    # Check for submission prompt keywords
                    submission_keywords = [
                        "submit application",
                        "ready to submit",
                        "would you like me to click",
                        "would you like me to submit",
                        "confirm submission"
                    ]
                    
                    if any(keyword in message_text for keyword in submission_keywords):
                        print(f"🎯 Detected submission prompt: {message_text[:100]}...")
                        time.sleep(0.5)  # Small delay to ensure UI is ready
                        
                        if find_and_fill_prompt_box(driver):
                            print("✅ Successfully sent confirmation")
                            time.sleep(5)  # Wait for agent to process
                        else:
                            print("⚠️ Could not find prompt box")
                except Exception as e:
                    print(f"Error reading message: {e}")
            
            # Also monitor for the specific LinkedIn context
            try:
                # Look for LinkedIn-specific elements that indicate a submission is ready
                page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                if "director of marketing" in page_text or "submit application" in 
page_text:
                    # Double-check if prompt box is available
                    if find_and_fill_prompt_box(driver):
                        print("✅ Preemptively sent confirmation based on context")
                        time.sleep(5)
            except:
                pass
                
        except Exception as e:
            print(f"Monitor error: {e}")
        
        time.sleep(1)  # Check every second

def main():
    print("Starting ChatGPT Agent Auto-Confirmer...")
    
    # Connect to existing Chrome instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"ERROR: Could not connect to Chrome. Is it running with 
--remote-debugging-port=9222?")
        print(f"Error details: {e}")
        return
    
    print("✅ Connected to Chrome")
    print("📍 Monitoring for submission prompts...")
    print("Press Ctrl+C to stop")
    
    try:
        monitor_for_submission_prompt(driver)
    except KeyboardInterrupt:
        print("\n👋 Stopping monitor")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
