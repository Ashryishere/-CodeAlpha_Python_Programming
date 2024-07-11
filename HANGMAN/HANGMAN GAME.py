import random
import tkinter as tk
from tkinter import messagebox
import pygame

# List of words for single player mode
word_list = ["python", "hangman", "challenge", "computer", "programming",
             "algorithm", "debugging", "function", "variable", "loop",
             "condition", "syntax", "recursion", "inheritance", "class",
             "object", "exception", "module", "package", "library"]

def switch_frame(frame):
    frame.tkraise()

def start_single_player():
    global word
    word = random.choice(word_list).lower()
    switch_frame(single_player_frame)
    start_game()

def start_multiplayer():
    switch_frame(multiplayer_frame)

def submit_word():
    global word
    word = word_entry.get().lower()
    switch_frame(single_player_frame)
    start_game()

def display_word(word, guesses):
    return ' '.join([letter if letter in guesses else '_' for letter in word])

def check_guess():
    global current_player
    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)

    if guess in guessed_letters or guess in incorrect_guesses:
        messagebox.showinfo("Hangman", "You've already guessed that letter.")
        return

    if guess in word:
        guessed_letters.add(guess)
        pygame.mixer.Sound.play(correct_sound)
    else:
        incorrect_guesses.add(guess)
        pygame.mixer.Sound.play(incorrect_sound)
        update_hangman()

    current_display = display_word(word, guessed_letters)
    word_label.config(text=current_display)

    if '_' not in current_display:
        scores[current_player] += 1
        pygame.mixer.Sound.play(win_sound)
        messagebox.showinfo("Hangman", f"Congratulations {players[current_player]}! You've guessed the word!")
        next_round()
    elif len(incorrect_guesses) >= attempts:
        pygame.mixer.Sound.play(lose_sound)
        messagebox.showinfo("Hangman", f"Game over {players[current_player]}. The word was: {word}")
        next_round()

def update_hangman():
    hangman_canvas.delete("all")
    hangman_canvas.create_line(20, 150, 100, 150, fill="black", width=2)  # base
    hangman_canvas.create_line(60, 150, 60, 20, fill="black", width=2)   # pole
    hangman_canvas.create_line(60, 20, 120, 20, fill="black", width=2)   # top beam
    hangman_canvas.create_line(120, 20, 120, 40, fill="black", width=2)  # rope

    if len(incorrect_guesses) > 0:
        hangman_canvas.create_oval(110, 40, 130, 60, outline="black", width=2)  # head
    if len(incorrect_guesses) > 1:
        hangman_canvas.create_line(120, 60, 120, 100, fill="black", width=2)   # body
    if len(incorrect_guesses) > 2:
        hangman_canvas.create_line(120, 70, 100, 90, fill="black", width=2)    # left arm
    if len(incorrect_guesses) > 3:
        hangman_canvas.create_line(120, 70, 140, 90, fill="black", width=2)    # right arm
    if len(incorrect_guesses) > 4:
        hangman_canvas.create_line(120, 100, 100, 130, fill="black", width=2)  # left leg
    if len(incorrect_guesses) > 5:
        hangman_canvas.create_line(120, 100, 140, 130, fill="black", width=2)  # right leg

def next_round():
    global current_player, guessed_letters, incorrect_guesses
    guessed_letters = set()
    incorrect_guesses = set()
    current_player = (current_player + 1) % 2
    update_scoreboard()
    choose_word() # type: ignore

def update_scoreboard():
    scoreboard.config(text=f"Score: {players[0]} {scores[0]} - {players[1]} {scores[1]}")

def start_game():
    update_hangman()
    update_scoreboard()
    word_label.config(text=display_word(word, guessed_letters))

pygame.init()
pygame.mixer.init()
correct_sound = pygame.mixer.Sound(r"HANGMAN/sounds/c.wav")
incorrect_sound = pygame.mixer.Sound(r"HANGMAN/sounds/I.wav")
win_sound = pygame.mixer.Sound(r"HANGMAN/sounds/W.wav")
lose_sound = pygame.mixer.Sound(r"/HANGMAN/sounds\L.wav")

players = ["Player 1", "Player 2"]
scores = [0, 0]
current_player = 0

guessed_letters = set()
incorrect_guesses = set()
attempts = 6

root = tk.Tk()
root.title("Hangman")
root.configure(bg='lightblue')

main_menu_frame = tk.Frame(root, bg='lightblue')
single_player_frame = tk.Frame(root, bg='lightblue')
multiplayer_frame = tk.Frame(root, bg='lightblue')

for frame in (main_menu_frame, single_player_frame, multiplayer_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Main menu frame
tk.Label(main_menu_frame, text="Welcome to Hangman", font=('Courier', 20), bg='lightblue').pack(pady=20)
tk.Button(main_menu_frame, text="Single Player", command=start_single_player, font=('Courier', 16), bg='green', fg='white').pack(pady=10)
tk.Button(main_menu_frame, text="Multiplayer", command=start_multiplayer, font=('Courier', 16), bg='blue', fg='white').pack(pady=10)

# Single player frame
scoreboard = tk.Label(single_player_frame, text="", font=('Courier', 16), bg='lightblue')
scoreboard.pack(pady=10)

hangman_canvas = tk.Canvas(single_player_frame, width=200, height=200, bg='lightblue')
hangman_canvas.pack(pady=10)

word_label = tk.Label(single_player_frame, text="", font=('Courier', 20), bg='lightblue')
word_label.pack(pady=10)

guess_entry = tk.Entry(single_player_frame, font=('Courier', 20), fg='blue')
guess_entry.pack(pady=10)
guess_entry.bind("<Return>", lambda event: check_guess())

guess_button = tk.Button(single_player_frame, text="Guess", command=check_guess, font=('Courier', 20), fg='white', bg='green')
guess_button.pack(pady=10)

tk.Button(single_player_frame, text="Back to Menu", command=lambda: switch_frame(main_menu_frame), font=('Courier', 16), bg='red', fg='white').pack(pady=10)

# Multiplayer frame
tk.Label(multiplayer_frame, text="Enter a word for your opponent to guess:", font=('Courier', 14), bg='lightblue').pack(pady=10)
word_entry = tk.Entry(multiplayer_frame, font=('Courier', 14))
word_entry.pack(pady=10)
tk.Button(multiplayer_frame, text="Submit", command=submit_word, font=('Courier', 14), bg='green', fg='white').pack(pady=10)

tk.Button(multiplayer_frame, text="Back to Menu", command=lambda: switch_frame(main_menu_frame), font=('Courier', 16), bg='red', fg='white').pack(pady=10)

switch_frame(main_menu_frame)

root.mainloop()
