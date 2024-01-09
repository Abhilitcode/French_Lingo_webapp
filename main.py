from tkinter import *
import pandas
import random
import pyttsx3
import smtplib


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
text_speech = pyttsx3.init()
text_speech.setProperty('rate', 120)
voices = text_speech.getProperty('voices')
text_speech.setProperty('voice', voices[0].id)
current_level = 2


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
    fr_text = current_card['French']
    print(fr_text)
    text_speech.say(fr_text)
    text_speech.runAndWait()
    print('spoke')


def is_known():
    if current_level == 1:
        to_learn.remove(current_card)
        print(len(to_learn))
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/alphabet_to_learn.csv", index=False)
        next_card()
    elif current_level == 2:
        to_learn.remove(current_card)
        print(len(to_learn))
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    elif current_level == 3:
        to_learn.remove(current_card)
        print(len(to_learn))
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/sentence_to_learn.csv", index=False)
        next_card()


def speak_french_word():
    text_speech.say(current_card['French'])
    text_speech.runAndWait()


def change_voice_to_male():
    all_voices = text_speech.getProperty('voices')
    text_speech.setProperty('voice', all_voices[0].id)


def speed_set(event):
    text_speech.setProperty('rate', slider_value.get())
    print('------------------------------------', slider_value.get())


def change_voice_to_female():
    all_voices = text_speech.getProperty('voices')
    text_speech.setProperty('voice', all_voices[1].id)


def level_1():
    global to_learn
    try:
        data = pandas.read_csv("data/alphabet_to_learn.csv")
    except FileNotFoundError:
        original_data = pandas.read_csv("data/french_alphabet.csv")
        print(original_data)
        to_learn = original_data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")
    finally:
        global current_level
        current_level = 1
        next_card()


def level_2():
    global to_learn
    try:
        data = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        original_data = pandas.read_csv("data/french_words.csv")
        print(original_data)
        to_learn = original_data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")
    finally:
        global current_level
        current_level = 2
        next_card()


def level_3():
    global to_learn
    try:
        data = pandas.read_csv("data/sentence_to_learn.csv")
    except FileNotFoundError:
        original_data = pandas.read_csv("data/french_sentence.csv")
        print(original_data)
        to_learn = original_data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")
    finally:
        global current_level
        current_level = 3
        next_card()


def send_email():
    print(email_entry.get())
    email = 'khaleabhishek351@gmail.com'
    app_pass_w = "zxnyhgddyhqvrdre"
    connection = smtplib.SMTP('smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(user=email, password=app_pass_w)
    connection.sendmail(from_addr=email, to_addrs=f'{email_entry.get()}',
                        msg=f"Subject:Frenchlingo for {current_card['French']}\n\n {current_card['French']} it means {current_card['English']} in english")
    print(email_entry.get())
    connection.close()


window = Tk()
window.title("French Lingo")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(2000, func=flip_card)


canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


email_label = Label(window, text='Email:')
email_label.place(x=300, y=530)

email_entry = Entry(window, width=30)
email_entry.place(x=342, y=530)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card, borderwidth=0)
unknown_button.grid(row=1, column=0)
speaker_image = PhotoImage(file='images/images_speaker (2).png')
speak_button = Button(image=speaker_image, command=speak_french_word, borderwidth=0)
speak_button.grid(row=1, column=3)


check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known, borderwidth=0)
known_button.grid(row=1, column=1)

slider_value = DoubleVar()

slider = Scale(window, from_=10, to=200, orient='horizontal', command=speed_set, variable=slider_value)
slider.place(x=800, y=400)


female_image = PhotoImage(file='images/female-figure (1).png')
female_button = Button(image=female_image ,highlightthickness=0, command=change_voice_to_female, borderwidth=0)
female_button.place(x=845, y=500)

male_image = PhotoImage(file='images/male-figure (1).png')
male_button = Button(image=male_image, highlightthickness=0, command=change_voice_to_male, borderwidth=0)
male_button.place(x=800, y=500)

level_1_image = PhotoImage(file='images/level 1 button raw (1).png')
level_1_button = Button(image=level_1_image, highlightthickness=0, command=level_1, borderwidth=0)
level_1_button.place(x=800, y=100)

email_image = PhotoImage(file='images/emale_logo.png')
email_button = Button(image=email_image, highlightthickness=0, command=send_email, borderwidth=0)
email_button.place(x=370, y=560)


level_2_image = PhotoImage(file='images/level 2 button raw (1).png')
level_2_button = Button(image=level_2_image, highlightthickness=0, command=level_2, borderwidth=0)
level_2_button.place(x=800, y=200)


level_3_image = PhotoImage(file='images/level3 button raw (1).png')
level_3_button = Button(image=level_3_image, highlightthickness=0, command=level_3, borderwidth=0)
level_3_button.place(x=800, y=300)
next_card()

window.mainloop()

