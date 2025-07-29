import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_inspector():
    print("Starting Deep Inspector Script...")
    
    # --- Connect to the browser ---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Successfully attached to the browser.")
    except Exception as e:
        print(f"FATAL ERROR: Could not connect. Is the browser running? Error: {e}")
        return

    print("\n" + "="*60)
    print("Attempting to dive into the nested iframe structure...")
    print("The 'Confirm' button should be visible on screen now.")
    print("="*60 + "\n")
    time.sleep(2)

    # --- The Inspection ---
    try:
        # Step 1: Switch to the top-level iframe (index 0)
        driver.switch_to.frame(0)
        
        # Step 2: Switch to the nested iframe (index 0)
        driver.switch_to.frame(0)
        
        print("--- SUCCESS: Successfully dived into nested iframe. ---")
        
        # Step 3: Find all buttons inside this frame
        print("\nSearching for all <button> elements inside this frame:")
        all_buttons = driver.find_elements(By.TAG_NAME, 'button')
        
        if not all_buttons:
            print("--> No <button> elements were found in this nested frame.")
        else:
            print(f"--> Found {len(all_buttons)} button(s). Their text is:")
            for i, btn in enumerate(all_buttons):
                # We also get the outerHTML to see the full tag
                print(f"  - Button #{i} Text: '{btn.text}'")
                print(f"    HTML: {btn.get_attribute('outerHTML')}\n")

    except Exception as e:
        print(f"\nERROR: Could not complete the inspection. The frame structure may have changed.")
        print(f"Details: {e}")
    
    finally:
        # Always switch back to the main page
        driver.switch_to.default_content()
        print("\n" + "="*60)
        print("Inspection complete.")
        print("="*60)
        driver.quit()

if __name__ == "__main__":
    run_inspector()

