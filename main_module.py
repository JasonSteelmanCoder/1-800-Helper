"""When someone has a 1-800 number, they often advertise it using a word. For example, 1-800-222-PAIN.
The word is made using the letters that would appear on a number pad for the digits in the phone number.

This program is meant to help a person who is choosing an available 1-800 number for their company. To 
accomplish that task, it will perform three main operations:

1. It will take a word as input and find the digits that correspond with it
2. It will take a description of the user's organization and ask ChatGPT for some good words to use
3. It will take a phone number as an input and find all of the words that can be spelled with those digits.

In each instance, the program will check if the resulting numbers are available, and, if a user selects
the number, it will simulate them purchasing the number."""

import sys
import tkinter as tk
from tkinter import messagebox
import available_num_finder as anf
import word_checker as wc
from chatgpt_api_caller import APICall

class PurchaseCompleteFrame(tk.Frame):
    def __init__(self, master):
        self.master = master

    def show_purchase_complete_frame(self, purchased_number):
        app.display_frame.clear_display()
        purchase_complete_label = tk.Label(app.display_frame, text=f"Congratulations!\nYou have successfully purchased the number:\n\n{purchased_number}\n\nClick a button on the left to find more numbers, OR\nClick the button below to leave the program.\n", pady=15)
        purchase_complete_label.pack()
        exit_button = tk.Button(app.display_frame, text="Exit", command=sys.exit)
        exit_button.config(width=15)
        exit_button.pack()

class Search():
    def __init__(self, search_term, event=None):
        self.search_term = search_term

    def show_overlong_word_message(self):
        overlong_word_label = tk.Label(app.display_frame, text="1-800 numbers only accommodate words up to seven letters long.\nPlease try a shorter word.")
        overlong_word_label.pack()

    def find_number_for_search_term(self):
        if len(self.search_term) > 7:
            self.show_overlong_word_message()
        desired_num = wc.find_num_for_word(self.search_term)
        app.search_frame.display_desired_num(desired_num)        
        for phone_number in app.available_numbers_long:
            number_found = False
            if phone_number.endswith(desired_num):
                number_found = True
                app.search_frame.display_search_results(phone_number)
                break
        if number_found == False:
            app.search_frame.display_search_results(None)

class SearchFrame(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

    def show_search_window(self):
        app.display_frame.clear_display()
        search_directions = tk.Label(app.display_frame, text="Enter a word here to see if it is available.\nNote: words must be 3-7 letters.")
        search_directions.pack(pady=40)
        self.search_box = tk.Entry(app.display_frame)
        self.search_box.pack(padx=20, pady=0)
        self.search_box.focus_set()
        self.search_box.bind('<Return>', lambda event=None: self.instantiate_search(event))

    def instantiate_search(self, event=None):
        self.clear_search_results()
        self.search = Search(self.search_box.get())
        self.search.find_number_for_search_term()

    def display_desired_num(self, desired_num):
        self.desired_num_label = tk.Label(app.display_frame, text=f"You are looking for a number ending with {desired_num}.")
        self.desired_num_label.pack()
    
    def display_search_results(self, number_results):
        if number_results:      # When the return is not None
            search_results = tk.Label(app.display_frame, text=f"The number you are looking for is available! It's {number_results}", fg="blue")
            search_results.pack()
            search_results.bind("<Button-1>", lambda event, number_results=number_results: app.display_frame.ask_user_to_purchase(number_results))
        else:
            sorry_message = tk.Label(app.display_frame, text="Sorry. That number is not available.\nTry another word, OR\nPress the button on the left to see words that are available.")
            sorry_message.pack()

    def clear_search_results(self):
        for i in range(len(app.display_frame.winfo_children())-1, -1, -1):
            if i > 1:
                app.display_frame.winfo_children()[i].destroy()

class ChatFrame(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master=master

    def show_chat_screen(self):
        app.display_frame.clear_display()
        self.chat_directions = tk.Label(app.display_frame, pady=20, text="Write a short description of your organization.\nInclude aspects that you would like to highlight in your marketing.\nThen press enter.")
        self.chat_directions.pack()
        example_text = "Example: At Those Who Wander Travel Agency, we'll never get you lost."
        self.chat_box = tk.Text(app.display_frame, wrap="word")
        self.chat_box.config(height=10, width=50)
        self.chat_box.pack()
        self.chat_box.insert(tk.END, example_text)
        self.chat_box.focus_set()
        self.chat_box.bind('<Return>', lambda event=None: self.get_chat_results())

    def get_chat_results(self):
        user_input = self.chat_box.get("1.0", "end-1c")
        api_call = APICall(user_input)
        self.display_chat_results(api_call.prepare_suggestions())

    def display_chat_results(self, suggestions:list):
        app.display_frame.clear_display()
        self.suggestions_header = tk.Label(app.display_frame, text="ChatGPT Says:  Number:  Availability\n", font=("courier", 9))
        self.suggestions_header.pack(anchor=tk.W)
        if suggestions:
            for word in suggestions:
                if len(word) < 8:   # Sometimes GPT suggests words that are too long
                    availability_message = None
                    available_num = wc.search_available_nums_for_word(word, app.available_numbers_long)
                    if available_num != None:
                        availability_message = "Available!"
                        font_color = "blue"
                        cursor_assignment = "hand2"
                        available_bool = True
                    else:
                        availability_message = "Not available."
                        font_color = "grey"
                        cursor_assignment = "arrow"
                        available_bool = False
                    label = tk.Label(app.display_frame, text=f"{word}{' '*(15-len(word))}{wc.find_num_for_word(word)}{' '*(9-len(word))}{availability_message}", fg=font_color, font=("courier", 9), cursor=cursor_assignment)
                    label.pack(anchor=tk.W)
                    if available_bool:
                        label.bind("<Button-1>", lambda event, phone_num=available_num: app.display_frame.ask_user_to_purchase(phone_num))
        else:
            self.error_label = tk.Label(app.display_frame, text="Sorry! Something went wrong. Please try again.")
            self.error_label.pack()

class ShowSomeAvailableWordsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master=master
        
    def show_some_available_words(self):
        app.display_frame.clear_display()
        self.display_wait_message()
        available_combos = {}
        for phone_num in app.number_retrieval.get_available_phone_nums_short(app.available_numbers_long):
            prepared_num = wc.prepare_phone_number(phone_num)
            temp_words = wc.find_words_for_num(prepared_num)
            if temp_words:
                temp_words.sort(key=len, reverse=True)
                available_combos[phone_num] = temp_words
        self.directions_label = tk.Label(app.display_frame, text="Here are some available numbers, and the words they spell.\n\nClick a number to purchase, OR\nClick Show_me_some_available_words again to see more.\n", pady=10)
        self.directions_label.pack()
        for selected_number, word_list in available_combos.items():
            label = tk.Label(app.display_frame, text=f"{selected_number}: {[word for word in word_list]}", cursor="hand2", fg="blue")
            label.pack(anchor=tk.W)
            label.bind("<Button-1>", lambda event, offered_number=selected_number: app.display_frame.ask_user_to_purchase(offered_number))
        self.destroy_wait_message()

    def display_wait_message(self):
        self.wait_message = tk.Label(app.display_frame, text="Finding available words...")
        self.wait_message.pack()
        self.update()

    def destroy_wait_message(self):
        self.wait_message.destroy()
        self.update()

class DisplayFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=450, highlightbackground="black", highlightthickness=1)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT)

    def clear_display(self):
        leftovers = self.winfo_children()
        for widget in leftovers:
            widget.destroy()
        self.update()

    def ask_user_to_purchase(self, offered_number, event=None):
        purchase_answer = messagebox.askyesno(f"Purchase number?", f"Do you want to purchase the number {offered_number}?")
        if purchase_answer:
            app.purchase_completion_frame.show_purchase_complete_frame(offered_number)

class MenuFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=250, bg="#4287f5")
        self.pack_propagate(False)
        self.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Chose what you want to do:", bg="#4287f5")
        self.label.pack(pady=30)

        self.find_num_button = tk.Button(self, text="Check if my word is available.", command=lambda: app.search_frame.show_search_window())
        self.find_num_button.config(width=24, height=2)
        self.find_num_button.pack(pady=10)

        self.suggest_word_button = tk.Button(self, text="Suggest some words.\n(Powered by ChatGPT)", command=lambda: app.chat_frame.show_chat_screen())
        self.suggest_word_button.config(width=24)
        self.suggest_word_button.pack(pady=10)

        self.find_word_button = tk.Button(self, text="Show me some available words.", command=lambda: app.show_some_available_words_frame.show_some_available_words())
        self.find_word_button.config(width=24, height=2)
        self.find_word_button.pack(pady=10)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("1-800 Number Finder")

        self.menu_frame = MenuFrame(master=self)
        self.display_frame = DisplayFrame(master=self)
        self.chat_frame = ChatFrame(master=self.display_frame)
        self.show_some_available_words_frame = ShowSomeAvailableWordsFrame(master=self.display_frame)
        self.search_frame = SearchFrame(master=self.display_frame)
        self.purchase_completion_frame = PurchaseCompleteFrame(master=self.display_frame)

        self.number_retrieval = anf.NumberRetrieval()
        self.available_numbers_long = self.number_retrieval.get_available_phone_nums_long()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# TODO:
# - write unit tests
# - add docstrings for each function

