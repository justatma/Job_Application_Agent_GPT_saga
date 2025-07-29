import pyautogui
import time

print("Mouse Coordinate Locator")
print("Move your mouse over the target element and note the X, Y coordinates.")
print("Press Ctrl-C to quit.")

try:
    while True:
        # Get and print the current mouse coordinates.
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nDone.')
