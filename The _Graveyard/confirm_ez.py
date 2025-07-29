#!/usr/bin/env python3
"""
confirm_ez.py
Auto-types 'yes' when ChatGPT agent asks for submission confirmation
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Connect to Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

print("Connected. Monitoring for submission prompts...")
print("Looking for: 'Please let me know if you'd like me to click'")

last_message_count = 0

while True:
    try:
        # Find all assistant messages
        messages = driver.find_elements(By.CSS_SELECTOR, "[data-message-author-role='assistant']")
        
        # Check if there are new messages
        if len(messages) > last_message_count:
            last_message_count = len(messages)
            
            # Check the last message
            last_msg = messages[-1]
            msg_text = last_msg.text
            
            # Look for the submission phrase
            if "Please let me know if you'd like me to click" in msg_text and "Submit application" in msg_text:
                print(f"🎯 Found submission prompt!")
                
                # Small delay
                time.sleep(0.5)
                
                try:
                    # Find the ProseMirror div by its exact class and id
                    prompt_box = driver.find_element(By.CSS_SELECTOR, "div.ProseMirror#prompt-textarea[contenteditable='true']")
                    
                    # Method 1: Click on it first to ensure focus
                    prompt_box.click()
                    time.sleep(0.1)
                    
                    # Method 2: Use JavaScript to set the content directly
                    driver.execute_script("""
                        var element = arguments[0];
                        element.focus();
                        element.innerHTML = '<p>yes</p>';
                        
                        // Trigger input event
                        var event = new Event('input', { bubbles: true });
                        element.dispatchEvent(event);
                        
                        // Trigger change event
                        var changeEvent = new Event('change', { bubbles: true });
                        element.dispatchEvent(changeEvent);
                    """, prompt_box)
                    
                    time.sleep(0.1)
                    
                    # Send Enter key
                    prompt_box.send_keys(Keys.RETURN)
                    
                    print("✅ Sent 'yes' confirmation!")
                    time.sleep(10)  # Wait longer before checking again
                    
                except Exception as e:
                    print(f"Primary method failed: {e}")
                    
                    # Fallback: Try using ActionChains
                    try:
                        prompt_box = driver.find_element(By.ID, "prompt-textarea")
                        actions = ActionChains(driver)
                        actions.move_to_element(prompt_box)
                        actions.click()
                        actions.send_keys("yes")
                        actions.send_keys(Keys.RETURN)
                        actions.perform()
                        print("✅ Sent 'yes' via ActionChains!")
                        time.sleep(10)
                    except Exception as e2:
                        print(f"Fallback also failed: {e2}")
    
    except Exception as e:
        # Silent fail to keep monitoring
        pass
    
    time.sleep(0.3)  # Check ~3 times per second

print("Monitor stopped.")
