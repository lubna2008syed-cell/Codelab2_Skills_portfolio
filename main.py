"""
Exercise 1 - Maths Quiz
A maths quiz made using Tkinter.
The player answers 10 addition or subtraction questions.
"""

import tkinter as tk
from tkinter import messagebox
import random

# Colours used in the quiz
BG_COLOUR = "#EAE2F4"
BUTTON_COLOUR = "#796391"
TEXT_COLOUR = "#49385E"
WHITE = "#FFFFFF"

# Quiz variables
TOTAL_QUESTIONS = 10

difficulty = 1
score = 0
questionNumber = 0
attempt = 1
correctAnswer = 0
answerEntry = None
attemptLabel = None
scoreLabel = None

# Create the main window
window = tk.Tk()
window.title("Maths Quiz")
window.geometry("420x390")
window.resizable(False, False)
window.configure(bg=BG_COLOUR)

# Remove the widgets from the current screen
def clearWindow():
    for widget in window.winfo_children():
        widget.destroy()

# Display the difficulty menu
def displayMenu():
    clearWindow()

    tk.Label(
        window,
        text="MATHS QUIZ",
        font=("Arial", 23, "bold"),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=(25, 8))

    tk.Label(
        window,
        text="Choose your difficulty level",
        font=("Arial", 13),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=10)

    tk.Button(
        window, text="Easy - 1 Digit",
        width=22, font=("Arial", 12),
        bg=BUTTON_COLOUR, fg=WHITE,
        command=lambda: startQuiz(1)
    ).pack(pady=7)

    tk.Button(
        window, text="Moderate - 2 Digits",
        width=22, font=("Arial", 12),
        bg=BUTTON_COLOUR, fg=WHITE,
        command=lambda: startQuiz(2)
    ).pack(pady=7)

    tk.Button(
        window, text="Advanced - 4 Digits",
        width=22, font=("Arial", 12),
        bg=BUTTON_COLOUR, fg=WHITE,
        command=lambda: startQuiz(3)
    ).pack(pady=7)

# Generate random numbers based on the difficulty
def randomInt(level):
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

# Randomly choose addition or subtraction
def decideOperation():
    return random.choice(["+", "-"])

# Display a maths question
def displayProblem():
    global questionNumber, attempt, correctAnswer
    global answerEntry, attemptLabel, scoreLabel

    clearWindow()

    questionNumber += 1
    attempt = 1

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    if operation == "+":
        correctAnswer = num1 + num2
    else:
        correctAnswer = num1 - num2

    tk.Label(
        window,
        text=f"Question {questionNumber} of {TOTAL_QUESTIONS}",
        font=("Arial", 14),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=(20, 5))

    scoreLabel = tk.Label(
        window,
        text=f"Score: {score}",
        font=("Arial", 12),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    )
    scoreLabel.pack(pady=5)

    tk.Label(
        window,
        text=f"{num1} {operation} {num2} = ?",
        font=("Arial", 27, "bold"),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=20)

    answerEntry = tk.Entry(
        window,
        font=("Arial", 18),
        width=10,
        justify="center",
        bg=WHITE,
        fg=TEXT_COLOUR
    )
    answerEntry.pack(pady=5)
    answerEntry.focus()

    answerEntry.bind("<Return>", lambda event: submitAnswer())

    attemptLabel = tk.Label(
        window,
        text="Attempt 1 of 2",
        font=("Arial", 11),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    )
    attemptLabel.pack(pady=10)

    tk.Button(
        window,
        text="Submit",
        font=("Arial", 12),
        width=14,
        bg=BUTTON_COLOUR,
        fg=WHITE,
        command=submitAnswer
    ).pack(pady=5)

# Check whether the player's answer is correct
def isCorrect(userAnswer, rightAnswer, tryNumber):
    if userAnswer == rightAnswer:
        if tryNumber == 1:
            messagebox.showinfo("Correct", "Well done! You earned 10 points.")
        else:
            messagebox.showinfo("Correct", "Correct! You earned 5 points.")
        return True

    if tryNumber == 1:
        messagebox.showwarning(
            "Wrong Answer",
            "That's not correct. You have one more chance!"
        )
    else:
        messagebox.showerror(
            "Wrong Answer",
            f"Sorry! The correct answer was {rightAnswer}."
        )

    return False

# Move to the next question or show the final results
def nextQuestion():
    if questionNumber < TOTAL_QUESTIONS:
        displayProblem()
    else:
        displayResults()

# Accept and check the player's answer
def submitAnswer():
    global score, attempt

    text = answerEntry.get().strip()

    try:
        userAnswer = int(text)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a whole number."
        )
        answerEntry.delete(0, tk.END)
        return

    if isCorrect(userAnswer, correctAnswer, attempt):

        if attempt == 1:
            score += 10
        else:
            score += 5

        nextQuestion()

    else:
        if attempt == 1:
            attempt = 2
            attemptLabel.config(text="Attempt 2 of 2")
            answerEntry.delete(0, tk.END)
            answerEntry.focus()
        else:
            nextQuestion()

# Display the final score and grade
def displayResults():
    clearWindow()

    if score > 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    tk.Label(
        window,
        text="QUIZ COMPLETE!",
        font=("Arial", 22, "bold"),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=(35, 15))

    tk.Label(
        window,
        text=f"Your score: {score} / 100",
        font=("Arial", 16),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=8)

    tk.Label(
        window,
        text=f"Your grade: {grade}",
        font=("Arial", 21, "bold"),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=8)

    tk.Label(
        window,
        text="Would you like to play again?",
        font=("Arial", 12),
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    ).pack(pady=15)

    tk.Button(
        window,
        text="Play Again",
        width=15,
        font=("Arial", 12),
        bg=BUTTON_COLOUR,
        fg=WHITE,
        command=displayMenu
    ).pack(pady=5)

    tk.Button(
        window,
        text="Quit",
        width=15,
        font=("Arial", 12),
        bg=BUTTON_COLOUR,
        fg=WHITE,
        command=window.destroy
    ).pack(pady=5)

# Start a new quiz
def startQuiz(level):
    global difficulty, score, questionNumber

    difficulty = level
    score = 0
    questionNumber = 0

    displayProblem()

# Start the program
displayMenu()
window.mainloop()