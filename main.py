import tkinter
from tkinter import *
import pandas
from random import randint

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
CHOICE_FONT = ("Ariel", 40, "bold")

flip_timer = None
foreign_language = ""
known_language = ""
current_card = ""
list_translations = []

card_image = None
language_text = ""
word_text = ""


# ------------- CHOOSE LANGUAGE FILE ------------- #
def choose_language_settings(language):
    """According to choice of language button, set language elements on interface"""
    global foreign_language, known_language, current_card, list_translations
    global card_image, language_text, word_text
    global flip_timer

    # Read data according to language
    # If progress file exists, read from this file, else read from the original file according to language
    input_file = ""
    try:
        with open(f"data/{language}_words_to_learn.csv"):
            input_file = f"data/{language}_words_to_learn.csv"
    except FileNotFoundError:
        input_file = f"data/{language}_words.csv"
    finally:
        data = pandas.read_csv(input_file)

    list_translations = pandas.DataFrame(data).to_dict(orient="records")  # generate a list of dictionaries

    # Set the chosen pair of languages
    foreign_language = list(list_translations[0])[0]  # take first key from first dictionary as foreign language
    known_language = list(list_translations[0])[1]  # take second key from first dictionary as translate language
    current_card = list_translations[0]

    # Clear the interface
    choice_label.pack_forget()
    french_button.pack_forget()
    german_button.pack_forget()
    romanian_button.pack_forget()
    spain_button.pack_forget()

    # Add card image with language and current word text
    card_image = canvas.create_image(400, 263, image=card_front_image)
    language_text = canvas.create_text(400, 150, text=foreign_language, font=LANGUAGE_FONT)
    word_text = canvas.create_text(400, 263, text=current_card[foreign_language], font=WORD_FONT)

    # Show the wrong and right buttons
    wrong_button.grid(column=0, row=1)
    right_button.grid(column=1, row=1)

    # Start the 3 seconds timer for flipping first card
    flip_timer = window.after(3000, flip_card)


# -------------- CREATE FLASH CARDS -------------- #
def generate_next_card(button_type):
    """Chooses another random card from list and update the widgets data from canvas"""
    global flip_timer, current_card
    window.after_cancel(flip_timer)

    # If user presses right button, this known word will be removed from the list of cards and
    # an updated file for learning will be generated
    # This has in scope to be shown only the words that user doesn't know
    if button_type == "right":
        list_translations.remove(current_card)
        data_to_learn = pandas.DataFrame(list_translations)
        data_to_learn.to_csv(f"data/{foreign_language.lower()}_words_to_learn.csv", index=False)

    current_card = list_translations[randint(1, len(list_translations) - 1)]
    word = current_card[foreign_language]

    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(language_text, text=foreign_language, fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")
    flip_timer = window.after(3000, flip_card)


# ------------------ FLIP CARD ------------------- #
def flip_card():
    """Flips the card with the translation data"""
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(language_text, text=known_language, fill="white")
    canvas.itemconfig(word_text, text=current_card[known_language], fill="white")


# ------------------- UI SETUP ------------------- #
window = Tk()
window.title("Flash cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50, width=900, height=726)
window.iconbitmap("images/icon_app.ico")

# Images
cross_image = PhotoImage(file="images/wrong.png")
check_image = PhotoImage(file="images/right.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
france_image = PhotoImage(file="images/france.png")
germany_image = PhotoImage(file="images/germany.png")
romania_image = PhotoImage(file="images/romania.png")
spain_image = PhotoImage(file="images/spain.png")

# Canvas with language buttons for first interface
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
choice_label = Label(canvas, text="Choose a language to learn:", font=LANGUAGE_FONT, bg=BACKGROUND_COLOR)
choice_label.pack(padx=50, pady=14)
french_button = Button(canvas, padx=95, text="French", width=155, height=70, image=france_image, highlightthickness=0,
                       border=0, bg=BACKGROUND_COLOR, fg="black", compound=tkinter.RIGHT, font=CHOICE_FONT,
                       command=lambda language="french": choose_language_settings(language))
french_button.pack(padx=50, pady=21)
german_button = Button(canvas, padx=75, text="German", width=200, height=70, image=germany_image, highlightthickness=0,
                       border=0, bg=BACKGROUND_COLOR, fg="black", compound=tkinter.RIGHT, font=CHOICE_FONT,
                       command=lambda language="german": choose_language_settings(language))
german_button.pack(padx=50, pady=27)
romanian_button = Button(canvas, padx=20, text="Romanian", width=305, height=70, image=romania_image,
                         highlightthickness=0, border=0, bg=BACKGROUND_COLOR, fg="black", compound=tkinter.RIGHT,
                         font=CHOICE_FONT, justify="left",
                         command=lambda language="romanian": choose_language_settings(language))
romanian_button.pack(padx=50, pady=33)
spain_button = Button(canvas, padx=135, text="Spain", width=80, height=70, image=spain_image, highlightthickness=0,
                      border=0, bg=BACKGROUND_COLOR, fg="black", compound=tkinter.RIGHT, font=CHOICE_FONT,
                      command=lambda language="spanish": choose_language_settings(language))
spain_button.pack(padx=50, pady=37)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons for second interface
wrong_button = Button(image=cross_image, highlightthickness=0, border=0,
                      command=lambda button_type="wrong": generate_next_card(button_type))
right_button = Button(image=check_image, highlightthickness=0, border=0,
                      command=lambda button_type="right": generate_next_card(button_type))

window.mainloop()
