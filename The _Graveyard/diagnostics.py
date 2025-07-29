import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_diagnostics():
    print("Starting Diagnostics Script...")
    
    # --- Connect to the browser ---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Successfully attached to the browser.")
    except Exception as e:
        print(f"FATAL ERROR: Could not connect to browser. Is it running? Error: {e}")
        return

    print("\n" + "="*60)
    print("Page Title:", driver.title)
    print("Scanning for iframes and buttons... Please ensure the 'Retry' or 'Confirm' button is visible on screen.")
    print("="*60 + "\n")
    time.sleep(3) # Give a moment for observation

    # --- The Investigation ---
    try:
        # Step 1: Get all top-level iframes
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        print(f"Found {len(iframes)} top-level iframe(s) on the page.")

        if not iframes:
            print("\nNo iframes found on the main page. This is unexpected.")
            print("Searching for the button on the main page content...")
            # If no frames, let's just check the main document
            buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Retry') or contains(., 'Confirm')]")
            if buttons:
                print(f"SUCCESS: Found {len(buttons)} button(s) on the main page itself!")
                for btn in buttons:
                    print(f" -> Button text: '{btn.text}'")
            else:
                 print("-> No 'Retry' or 'Confirm' button found on the main page.")
            return

        # Step 2: Loop through each iframe and inspect it
        for i, frame in enumerate(iframes):
            frame_id = frame.get_attribute('id')
            frame_src = frame.get_attribute('src')
            print(f"\n--- Checking Top-Level IFrame #{i} ---")
            print(f"  ID: '{frame_id}'")
            print(f"  SRC: '{frame_src}'")
            
            # Step 3: Switch into the iframe
            driver.switch_to.frame(i)
            
            # Step 4: Search for the button INSIDE this iframe
            buttons_in_frame = driver.find_elements(By.XPATH, "//button[contains(., 'Retry') or contains(., 'Confirm')]")
            
            if buttons_in_frame:
                print(f"  SUCCESS! Found the button inside this iframe (Top-Level IFrame #{i})!")
                for btn in buttons_in_frame:
                     print(f"  -> Button text: '{btn.text}'")
            else:
                print("  -> Button not found in this iframe. Checking for nested iframes...")
                
                # Step 5: Check for NESTED iframes
                nested_frames = driver.find_elements(By.TAG_NAME, 'iframe')
                if nested_frames:
                    print(f"  -> Found {len(nested_frames)} nested iframe(s) inside Top-Level IFrame #{i}.")
                    # In a real scenario, you'd loop through these too, but for now, this confirms their existence.
                else:
                    print("  -> No nested iframes found here.")

            # Step 6: CRUCIAL - Switch back to the main page before checking the next iframe
            driver.switch_to.default_content()

    except Exception as e:
        print(f"\nAn error occurred during diagnostics: {e}")
    
    finally:
        print("\n" + "="*60)
        print("Diagnostics complete.")
        print("="*60)
        driver.quit()

if __name__ == "__main__":
    run_diagnostics()
