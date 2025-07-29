import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
CONFIRM_BUTTON_DAY_IMAGE = 'confirm_button_day.png'
CONFIRM_BUTTON_NIGHT_IMAGE = 'confirm_button_night.png'
RETRY_BUTTON_XPATH = "//button[normalize-space()='Retry']"

# --- Coordinate data from your diagnostic ---
# The dynamic search region for the visual search
SEARCH_REGION = (47, 116, 1510, 849) # (Left_X, Top_Y, Width, Height)

# The "last resort" hardcoded coordinates for the confirm button
CONFIRM_BUTTON_COORDS = (509, 615) # (X, Y)


# --- Main Automation Script ---
if __name__ == "__main__":
    print("Starting Failsafe Visual Automator...")
    
    # --- Connect to Browser ---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Successfully attached. Monitoring all states.")
    except Exception as e:
        print(f"\nFATAL ERROR: Could not connect. Is the browser running? Error: {e}")
        exit()

    print("\n" + "="*60)
    print("Monitoring with Failsafe Logic (Visual Search -> Coordinate Click).")
    print("Press Ctrl-C to stop.")
    print("="*60 + "\n")

    clicked_fallback = False

    while True:
        try:
            # --- Priority 1: Visual Search for the Confirm button ---
            button_location = None
            try:
                # First, try day mode button inside our defined region
                button_location = pyautogui.locateOnScreen(
                    CONFIRM_BUTTON_DAY_IMAGE,
                    region=SEARCH_REGION,
                    grayscale=True,
                    confidence=0.8
                )
                if button_location is None:
                    # If not found, try night mode button
                    button_location = pyautogui.locateOnScreen(
                        CONFIRM_BUTTON_NIGHT_IMAGE,
                        region=SEARCH_REGION,
                        grayscale=True,
                        confidence=0.8
                    )
            except pyautogui.PyAutoGUIException:
                pass 

            if button_location:
                print("SUCCESS (Visual Search): 'Confirm' button found! Clicking.")
                button_center = pyautogui.center(button_location)
                pyautogui.click(button_center)
                print("--> Confirmation sent.")
                clicked_fallback = False # Reset fallback flag
                time.sleep(5)
                continue

            # --- Priority 2: Coordinate Click as a Fallback ---
            # This runs only if the visual search fails. We will try this ONCE.
            if not clicked_fallback:
                # Check if a pixel at the button's location is either white (day) or black (night)
                # This is a safety check to avoid clicking randomly.
                pixel_color = pyautogui.pixel(CONFIRM_BUTTON_COORDS[0], CONFIRM_BUTTON_COORDS[1])
                # Check if the pixel is very light (day mode) or very dark (night mode)
                if pixel_color[0] > 200 or pixel_color[0] < 50: 
                    print("WARN (Fallback): Visual search failed. Attempting coordinate click...")
                    pyautogui.click(CONFIRM_BUTTON_COORDS)
                    print("--> Fallback confirmation sent.")
                    clicked_fallback = True # Set flag so we don't click this again
                    time.sleep(5)
                    continue

            # --- Priority 3: Check for Selenium 'Retry' button ---
            try:
                driver.switch_to.default_content()
                retry_button = driver.find_element(By.XPATH, RETRY_BUTTON_XPATH)
                print("WARN (Platform): Disconnect detected! Clicking 'Retry'...")
                retry_button.click()
                print("--> Connection re-established.")
                clicked_fallback = False # Reset fallback on platform error
                time.sleep(5)
            except:
                pass

        except KeyboardInterrupt:
            print("\nScript stopped by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            time.sleep(3)
        
        time.sleep(2)

    print("Script finished.")
