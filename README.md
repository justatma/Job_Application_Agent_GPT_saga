# The Peterkin Protocol: 

How a 9-Line Script Outsmarted a Team of AIs to Automate the Un-Automatable

### 1. The Premise: A Peterkin Paper for the Digital Age

For three days, our crack team—one human engineer flanked by three of the most powerful AIs on the planet—attempted to automate a single confirmation prompt. We mapped the DOM. We wrote code elegant and ugly. We summoned silicon intelligence from the clouds, only to watch each attempt dissolve in the sandtraps of a hard-coded, human-required UI intervention. At last—after 50 false starts and with dignity in tatters—it struck me: I'll just make the computer *think* my finger pressed the keys.

Much like the famous Peterkin family, who once called a family council to solve the problem of salt in their morning coffee (and consulted half the town before someone suggested making a new pot), we applied every ounce of technical sophistication to a deceptively simple task. This repository is the story of that journey and the laughably simple solution that finally worked.

### 2. The Peterkin Dilemma: The Unclickable Prompt

The goal was simple: create a fully autonomous agent to apply for jobs on LinkedIn. The system involved two parts:

1. **The Agent (OpenAI's ChatGPT Agent):** A powerful AI tasked with navigating LinkedIn, finding jobs, and filling out complex application forms.

2. **The Automator (Our Python Script):** A helper script designed to handle the one thing the agent was explicitly forbidden from doing: giving the final confirmation to submit an application.

The problem was a feature, not a bug. The agent was hard-wired to stop and await human input. Our job was to build the "human."

### 3. Our Descent into Madness: A Chronicle of Failed Brilliance

For three days, we became honorary Peterkins. Our team consisted of one human engineer and a formidable trio of AIs: **Google's Gemini**, **Anthropic's Claude 3 Opus**, and **Kimi AI's K2**—three of the most highly-rated AI Python engineers on the planet.

Together, we embarked on a quest of epic over-engineering. We scoured the DOM, battled iframes, raised API tickets, and dreamed in XPath. Our chronicle of failed attempts included:

- **The Diplomat:** Trying to reason with the agent via increasingly forceful and complex prompts. (Result: The agent politely informed us its safety protocols were non-negotiable).

- **The Architect:** Meticulously mapping the page's structure, only to find the target button lived in a phantom world of iframes, nested iframes, and Shadow DOMs that defied all standard Selenium locators.

- **The Exorcist:** Engaging in a prolonged battle with macOS's security demons, granting permissions for Screen Recording, Accessibility, and Input Monitoring to every conceivable application, followed by reboots and ritualistic system resets.

- **The Sharpshooter:** Abandoning code-based detection for high-fidelity visual recognition with pyautogui, only to be thwarted by the subtle artifacts of a remote VM's video stream.

- **The Brute:** A final, desperate attempt to click hard-coded screen coordinates, which the system simply ignored as if the click never happened.

After nearly 70 scripts, four brilliant minds (one human, three silicon), and endless debugging, we had not a single green checkmark in sight.

### 4. The Epiphany: Enter The Lady from Philadelphia

And then, it happened. The breakthrough came not with a technical revelation, but with the realization that we needed to stop thinking like software engineers for just one minute. The conversation went something like this:

*"The system is blocking our script's synthetic mouse clicks. But the agent's prompt just needs me to type 'confirm' or 'yes'... What if... what if the script just... typed?"*

The final, elegant answer—a mere nine lines of code—came not from the cathedral of code but from the village idiot who just happened to wander in and press the right keys. And reader, that idiot was me.

### 5. The Solution: The 9-Line Miracle

We stopped trying to *detect* the prompt. We stopped trying to *click* a button. We stopped trying to be smart. Instead, we wrote a simple, "dumb" script that does one thing: it simulates a keyboard and types a confirmation word every few minutes. It doesn't need to see the screen. It doesn't need to know the state of the agent. It just types.

And it works...

#### Generated python

```python
#!/usr/bin/env python3
"""
Yes02.py - Types 'yes' every 5 minutes to confirm agent prompts.
"""
import time
import pyautogui

print("The Peterkin Protocol is active...")
print("Will type 'yes' and press Enter every 5 minutes.")
print("Keep the ChatGPT Agent tab as the active window. Press Ctrl-C to stop.")

while True:
    time.sleep(300)  # Wait for 5 minutes
    print(f"Typing 'yes' at {time.strftime('%H:%M:%S')}")
    pyautogui.typewrite('yes')
    pyautogui.press('enter')
```

### 6. The Lesson: When You've Dug Forty Trenches, Turn on the Tap

Sometimes, the problem that confounds the most formidable minds is the one nobody dares to try because it's almost laughably direct. After attempting every sophisticated method in the book, the solution was not cleverer code, but a hint of common sense and a fresh perspective. We used a virtual hand to type on a virtual keyboard, automating what automation itself insisted remain manual.

The best solution, like the advice from the Lady from Philadelphia, is often hiding in plain sight—waiting for one more cup of coffee.
