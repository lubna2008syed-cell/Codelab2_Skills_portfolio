"""
Exercise 2 - Alexa tell me a Joke
A Tkinter joke-telling assistant. Jokes are read from randomJokes.txt,
where each line holds a setup and a punchline separated by a question mark.
"""

import tkinter as tk
from tkinter import messagebox
import random
import os

# ---------------------------------------------------------------
# Global variables
# ---------------------------------------------------------------
jokes = []              # list of (setup, punchline) pairs
currentPunchline = ""   # punchline of the joke currently on screen

# The joke file should be in the same folder as this script,
# or in a "resources" folder next to it (or one folder up).
scriptFolder = os.path.dirname(os.path.abspath(__file__))
possiblePaths = [
    os.path.join(scriptFolder, "randomJokes.txt"),
    os.path.join(scriptFolder, "resources", "randomJokes.txt"),
    os.path.join(scriptFolder, "..", "resources", "randomJokes.txt"),
]


# ---------------------------------------------------------------
# Functions
# ---------------------------------------------------------------
def loadJokes():
    """Read the joke file and return a list of (setup, punchline) tuples."""
    jokeList = []

    # Find the first path that exists
    filePath = None
    for path in possiblePaths:
        if os.path.exists(path):
            filePath = path
            break

    if filePath is None:
        return jokeList  # empty list: the caller will show an error

    with open(filePath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and lines with no question mark
            if line == "" or "?" not in line:
                continue

            # Remove the "- " at the start of the line if it is there
            if line.startswith("-"):
                line = line[1:].strip()

            # Split at the FIRST question mark only
            position = line.index("?")
            setup = line[:position + 1]               # keep the "?"
            punchline = line[position + 1:].strip()   # everything after it

            jokeList.append((setup, punchline))

    return jokeList


def tellJoke():
    """Pick a random joke and show only the setup."""
    global currentPunchline

    joke = random.choice(jokes)
    currentPunchline = joke[1]

    setupLabel.config(text=joke[0])
    punchlineLabel.config(text="")   # hide the previous punchline

    # Now that a joke is showing, the other buttons can be used
    punchlineButton.config(state="normal")
    nextButton.config(state="normal")


def showPunchline():
    """Show the punchline below the setup."""
    punchlineLabel.config(text=currentPunchline)
    punchlineButton.config(state="disabled")   # no need to click it twice


# ---------------------------------------------------------------
# Main window
# ---------------------------------------------------------------
window = tk.Tk()
window.title("Alexa Joke Assistant")
window.geometry("520x380")
window.resizable(False, False)

jokes = loadJokes()
if len(jokes) == 0:
    messagebox.showerror("File error",
                         "Could not load any jokes.\n"
                         "Make sure randomJokes.txt is in the same folder as this program.")
    window.destroy()
    raise SystemExit

tk.Label(window, text="Joke Assistant", font=("Arial", 22, "bold")).pack(pady=(20, 10))

# Starts the first joke
alexaButton = tk.Button(window, text="Alexa tell me a Joke", font=("Arial", 13),
                        width=22, command=tellJoke)
alexaButton.pack(pady=5)

# Labels for the setup and the punchline (wraplength stops long jokes running off screen)
setupLabel = tk.Label(window, text="", font=("Arial", 14), wraplength=460, height=3)
setupLabel.pack(pady=(15, 5))

punchlineLabel = tk.Label(window, text="", font=("Arial", 14, "italic"),
                          fg="darkgreen", wraplength=460, height=3)
punchlineLabel.pack(pady=5)

# Button row
buttonFrame = tk.Frame(window)
buttonFrame.pack(pady=15)

punchlineButton = tk.Button(buttonFrame, text="Show Punchline", font=("Arial", 12),
                            width=14, state="disabled", command=showPunchline)
punchlineButton.grid(row=0, column=0, padx=5)

nextButton = tk.Button(buttonFrame, text="Next Joke", font=("Arial", 12),
                       width=14, state="disabled", command=tellJoke)
nextButton.grid(row=0, column=1, padx=5)

quitButton = tk.Button(buttonFrame, text="Quit", font=("Arial", 12),
                       width=14, command=window.destroy)
quitButton.grid(row=0, column=2, padx=5)

window.geometry("560x380")
window.mainloop()