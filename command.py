"""When someone has a 1-800 number, they often advertise it using a word. For example, 1-800-222-PAIN.
The word is made using the letters that would appear on a number pad for the digits in the phone number.

This program is meant to help a person who is choosing an available 1-800 number for their company.
It will take a phone number as an input and find all of the words that can be spelled with those digits."""

import available_num_finder as anf
import word_checker as wc
import tkinter as tk
from chatgpt_api_caller import APICall

class Search():
    def __init__(self, search_term, event=None):
        self.search_term = search_term

    def find_word_for_search_term(self):
        app.display_frame.clear_search_results()
        desired_num = wc.find_num_for_word(self.search_term)

        app.display_frame.desired_num_label = tk.Label(app.display_frame, text=f"You are looking for a number ending with {desired_num}.")
        app.display_frame.desired_num_label.pack()
        
        for phone_number in app.available_numbers_long:
            number_found = False
            if phone_number.endswith(desired_num):
                number_found = True
                app.display_frame.display_search_results(phone_number)
                break
        if number_found == False:
            app.display_frame.display_search_results(None)

class DisplayFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=450, highlightbackground="black", highlightthickness=1)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT)

    def show_search_window(self):
        self.clear_display()
        search_directions = tk.Label(self, text="Enter a word here to see if it is available.\nNote: words must be 3-7 letters.")
        search_directions.pack(pady=40)
        self.search_box = tk.Entry(self)
        self.search_box.pack(padx=20, pady=0)
        self.search_box.focus_set()
        self.search_box.bind('<Return>', lambda event=None: self.start_search(event))

    def start_search(self, event=None):
        search = Search(self.search_box.get())
        search.find_word_for_search_term()

    def show_available_words(self):
        self.clear_display()
        self.display_wait_message()
        available_combos = {}
        for num in app.available_numbers_short:
            prepared_num = wc.prepare_phone_number(num)
            temp_words = wc.find_words_for_num(prepared_num)
            if temp_words:
                temp_words.sort(key=len, reverse=True)
                available_combos[num] = temp_words
        formatted_output = self.format_output(available_combos)
        available_combos_label = tk.Label(self, text=formatted_output, justify=tk.LEFT)
        available_combos_label.pack(pady=20)
        self.destroy_wait_message()

    def display_wait_message(self):
        self.wait_message = tk.Label(self, text="Finding available words...")
        self.wait_message.pack()
        self.update()

    def destroy_wait_message(self):
        self.wait_message.destroy()
        self.update()

    def clear_display(self):
        leftovers = self.winfo_children()
        for widget in leftovers:
            widget.destroy()
        self.update()

    def format_output(self, combos:dict) -> str:
        combo_list = []
        for item in combos.items():
            combo_list.append(str(item))
        combo_list.sort(key=len, reverse=True)
        combo_str = "\n".join(combo_list)
        return combo_str
    
    def display_search_results(self, number_results):
        if number_results:      # When the return is not None
            search_results = tk.Label(self, text=f"The number you are looking for is available! It's {number_results}")
            search_results.pack()
        else:
            sorry_message = tk.Label(self, text="Sorry. That number is not available.\nTry another word, OR\nPress the button on the left to see words that are available.")
            sorry_message.pack()

    def clear_search_results(self):
        for i in range(len(self.winfo_children())-1, -1, -1):
            if i > 1:
                self.winfo_children()[i].destroy()

    def show_chat_screen(self):
        self.clear_display()
        self.chat_directions = tk.Label(self, pady=20, text="Write a short description of your organization.\nInclude aspects that you would like to highlight in your marketing.\nThen press enter.")
        self.chat_directions.pack()
        example_text = "Example: At Those Who Wander Travel Agency, we'll never get you lost."
        self.chat_box = tk.Text(self, wrap="word")
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
        self.clear_display()
        self.suggestions_header = tk.Label(self, text="ChatGPT Says:  Number:  Availability\n", font=("courier", 9))
        self.suggestions_header.pack(anchor=tk.W)
        if suggestions:
            for word in suggestions:
                if len(word) < 8:   # Sometimes GPT suggests words that are too long
                    availability_message = None
                    available_num = wc.search_available_nums_for_word(word, app.available_numbers_long)
                    if available_num != None:
                        availability_message = "Available!"
                        font_color = "blue"
                    else:
                        availability_message = "Not available."
                        font_color = "grey"
                    label = tk.Label(self, text=f"{word}{' '*(15-len(word))}{wc.find_num_for_word(word)}{' '*(9-len(word))}{availability_message}", fg=font_color, font=("courier", 9))
                    label.pack(anchor=tk.W)
        else:
            self.error_label = tk.Label(self, text="Sorry! Something went wrong. Please try again.")
            self.error_label.pack()

class MenuFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=250, bg="#4287f5")
        self.pack_propagate(False)
        self.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Chose what you want to do:", bg="#4287f5")
        self.label.pack(pady=30)

        self.find_num_button = tk.Button(self, text="Check if my word is available.", command=lambda: app.display_frame.show_search_window())
        self.find_num_button.config(width=24, height=2)
        self.find_num_button.pack(pady=10)

        self.suggest_word_button = tk.Button(self, text="Suggest some words.\n(Powered by ChatGPT)", command=lambda: app.display_frame.show_chat_screen())
        self.suggest_word_button.config(width=24)
        self.suggest_word_button.pack(pady=10)

        self.find_word_button = tk.Button(self, text="Show me some available words.", command=lambda: app.display_frame.show_available_words())
        self.find_word_button.config(width=24, height=2)
        self.find_word_button.pack(pady=10)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("1-800 Number Finder")

        self.menu_frame = MenuFrame(master=self)
        self.display_frame = DisplayFrame(master=self)

        self.number_retrieval = anf.NumberRetrieval()
        self.available_numbers_long = self.number_retrieval.get_available_phone_nums_long()
        self.available_numbers_short = self.number_retrieval.get_available_phone_nums_short()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# TODO:
# - break display_frame into more manageable classes for each page

# - add layer where users can select the number they want to buy
# - make available chat display labels clickable
# - clean up display format for list of available numbers

# - add error handling for when users put in numbers that are too long, wrong type, etc.
# - fix the InvalidPhoneNumber exception in word_checker.py
# - write unit tests

# - clean up the comments
# - add docstrings for each function

