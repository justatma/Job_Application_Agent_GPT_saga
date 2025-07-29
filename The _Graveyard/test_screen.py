import pyautogui

print("Attempting to take a test screenshot...")

try:
    # This is the simplest pyautogui command that requires screen access.
    screenshot = pyautogui.screenshot()
    
    # If the above line works without error, the permission is fixed.
    print("\nSUCCESS! The script has screen access.")
    print("A test screenshot was taken successfully and saved as 'test_screenshot.png'.")
    screenshot.save("test_screenshot.png")
    
except Exception as e:
    print("\n--- FAILED ---")
    print("The script still does not have screen recording permissions.")
    print(f"Error details: {e}")

print("\nTest complete.")
