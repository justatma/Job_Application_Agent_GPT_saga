import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def run_shadow_inspector():
    print("Starting Shadow DOM Inspector...")
    
    # --- Connect to Browser ---
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
    print("Searching the entire page for Shadow DOMs...")
    print("The 'Confirm' button should be visible on screen.")
    print("="*60 + "\n")
    time.sleep(2)

    # This JavaScript code will find all elements on the page,
    # check if they have a shadowRoot, and if so, search inside for our button.
    js_script = """
    const searchInShadows = (root, query) => {
        let results = [];
        const elements = root.querySelectorAll('*');
        for (const el of elements) {
            if (el.shadowRoot) {
                const found = el.shadowRoot.querySelector(query);
                if (found) {
                    results.push({
                        host_tag: el.tagName,
                        host_id: el.id,
                        host_class: el.className,
                        button_html: found.outerHTML
                    });
                }
                // Recursive search
                results = results.concat(searchInShadows(el.shadowRoot, query));
            }
        }
        return results;
    };
    return searchInShadows(document, "button");
    """

    try:
        # Execute the script to find all buttons inside any shadow DOM
        found_elements = driver.execute_script(js_script)

        if not found_elements:
            print("--- RESULT: No 'Confirm' or 'Retry' buttons found inside any Shadow DOM. ---")
            print("This is very unexpected. The element might be created in a way that even this script cannot see.")
        else:
            print(f"--- SUCCESS! Found {len(found_elements)} potential target(s) inside Shadow DOMs! ---")
            for i, item in enumerate(found_elements):
                # We check if the button's HTML contains the text we want
                if 'Confirm' in item['button_html'] or 'Retry' in item['button_html']:
                    print(f"\n--- Potential Match #{i+1} ---")
                    print(f"  Button was found inside a Shadow DOM hosted by a <{item['host_tag'].lower()}> element.")
                    print(f"  Host Element ID: '{item['host_id']}'")
                    print(f"  Host Element Classes: '{item['host_class']}'")
                    print(f"  Found Button HTML: {item['button_html']}")
                

    except Exception as e:
        print(f"\nAn error occurred during the JavaScript inspection: {e}")
    
    finally:
        print("\n" + "="*60)
        print("Shadow DOM inspection complete.")
        print("="*60)
        driver.quit()

if __name__ == "__main__":
    run_shadow_inspector()
