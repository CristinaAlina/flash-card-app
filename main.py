from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")


# ------------------- UI SETUP ------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.iconbitmap("images/icon_app.ico")

# Images
cross_image = PhotoImage(file="images/wrong.png")
check_image = PhotoImage(file="images/right.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")

# Canvas with card image
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_front_image)
language_text = canvas.create_text(400, 150, text="Language", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, text="word", font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_button = Button(image=cross_image, highlightthickness=0, border=0)
wrong_button.grid(column=0, row=1)
right_button = Button(image=check_image, highlightthickness=0, border=0)
right_button.grid(column=1, row=1)

window.mainloop()
