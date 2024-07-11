import nltk
from nltk.chat.util import Chat, reflections
import requests
import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk
from datetime import datetime

nltk.download('punkt')

# Define API constants
API_KEY = '82711e16742b4c2aac94862453e57774'
BASE_URL = 'https://api.football-data.org/v4/'

# Define pairs of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I assist you with football information today?",]
    ],
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey! How can I help you with football today?"]
    ],
    [
        r"what is your name?",
        ["I am a football chatbot created by OpenAI. You can call me FootBot!",]
    ],
    [
        r"how are you?",
        ["I'm just a bunch of code, but I'm here to help you with football information!",]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day.",]
    ],
    [
        r"(.*)matches(.*)",
        ["Fetching live matches for you...",]
    ],
    [
        r"(.*)",
        ["I'm not sure I understand. Can you please rephrase?"]
    ],
]

suggested_questions = [
    "What are the current live matches?",
    "Tell me about the latest football news.",
    "Who is the top scorer this season?",
    "What are today's match results?",
]

def fetch_live_matches():
    headers = {
        'X-Auth-Token': API_KEY
    }
    current_date = datetime.now().strftime('%Y-%m-%d')
    params = {
        'dateFrom': current_date,
        'dateTo': current_date,
    }
    try:
        response = requests.get(BASE_URL + 'matches', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        matches = data.get('matches', [])
        live_matches = [match for match in matches if match['status'] == 'LIVE']
        if live_matches:
            return [f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} - {match['status']}" for match in live_matches]
        else:
            return ["No live matches found."]
    except requests.exceptions.RequestException as e:
        return [f"Error fetching live matches: {e}"]

# Extend the chatbot's functionality to handle live data requests
class FootballChat(Chat):
    def respond(self, str):
        if "matches" in str.lower():
            matches = fetch_live_matches()
            return "\n".join(matches)
        return super().respond(str)

# Initialize the chatbot
chatbot = FootballChat(pairs, reflections)

def send_message():
    user_input = user_entry.get()
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n", 'user')
    chat_window.configure(state=tk.DISABLED)
    
    response = chatbot.respond(user_input)
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, "Bot: " + response + "\n", 'bot')
    chat_window.insert(tk.END, "\nYou can ask me questions like:\n", 'suggest')
    for question in suggested_questions:
        chat_window.insert(tk.END, "- " + question + "\n", 'suggest')
    chat_window.configure(state=tk.DISABLED)
    
    user_entry.delete(0, tk.END)

# Create the GUI
root = tk.Tk()
root.title("Football Chatbot")

# Apply a football style background
bg_image = Image.open("Basic chatbot/football_bg.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)


style = ttk.Style()
style.configure("TFrame", background="#3E4149")
style.configure("TLabel", background="#3E4149", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TButton", background="#5E81AC", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TEntry", background="#4C566A", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TScrolledText", background="#2E3440", foreground="#D8DEE9", font=("Helvetica", 12))

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(pady=10)

chat_window = scrolledtext.ScrolledText(main_frame, state='disabled', width=80, height=20, wrap='word', bg="#2E3440", fg="#D8DEE9", font=("Helvetica", 12))
chat_window.tag_configure('user', foreground='#A3BE8C')
chat_window.tag_configure('bot', foreground='#88C0D0')
chat_window.tag_configure('suggest', foreground='#EBCB8B')
chat_window.pack(pady=10)

user_entry = ttk.Entry(main_frame, width=80)
user_entry.pack(pady=10)
user_entry.bind("<Return>", lambda event: send_message())

send_button = ttk.Button(main_frame, text="Send", command=send_message)
send_button.pack(pady=10)

def start_chat():
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, "Hi, I'm your football chatbot! Type 'quit' to exit.\n", 'bot')
    chat_window.insert(tk.END, "You can ask me questions like:\n", 'suggest')
    for question in suggested_questions:
        chat_window.insert(tk.END, "- " + question + "\n", 'suggest')
    chat_window.configure(state=tk.DISABLED)

if __name__ == "__main__":
    start_chat()
    root.mainloop()


# Apply a football style background
bg_image = Image.open("Basic chatbot/football_bg.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

style = ttk.Style()
style.configure("TFrame", background="#3E4149")
style.configure("TLabel", background="#3E4149", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TButton", background="#5E81AC", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TEntry", background="#4C566A", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TScrolledText", background="#2E3440", foreground="#D8DEE9", font=("Helvetica", 12))

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(pady=10)

chat_window = scrolledtext.ScrolledText(main_frame, state='disabled', width=80, height=20, wrap='word', bg="#2E3440", fg="#D8DEE9", font=("Helvetica", 12))
chat_window.tag_configure('user', foreground='#A3BE8C')
chat_window.tag_configure('bot', foreground='#88C0D0')
chat_window.tag_configure('suggest', foreground='#EBCB8B')
chat_window.pack(pady=10)

user_entry = ttk.Entry(main_frame, width=80)
user_entry.pack(pady=10)
user_entry.bind("<Return>", lambda event: send_message())

send_button = ttk.Button(main_frame, text="Send", command=send_message)
send_button.pack(pady=10)

def start_chat():
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, "Hi, I'm your football chatbot! Type 'quit' to exit.\n", 'bot')
    chat_window.insert(tk.END, "You can ask me questions like:\n", 'suggest')
    for question in suggested_questions:
        chat_window.insert(tk.END, "- " + question + "\n", 'suggest')
    chat_window.configure(state=tk.DISABLED)

if __name__ == "__main__":
    start_chat()
    root.mainloop()
