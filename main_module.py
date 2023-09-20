"""When someone has a 1-800 number, they often advertise it using a word. For example, 1-800-222-MOVE.
The word is made using the letters that would appear on a number pad for the digits in the phone number.

This program is meant to help a person who is choosing an available 1-800 number for their organization. 
To accomplish that task, it will perform three main operations:

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

"""This window appears in the display frame. It congratulates the user on having purchased a number and 
instructs them to either click exit or return to look for more numbers by clicking a button in the menu 
frame."""
class PurchaseCompleteWindow():
    def __init__(self, master):
        self.master = master

    def show_purchase_complete_frame(self, purchased_number):
        # A label congratulates the user and directs them to exit or click a button on the menu frame. 
        # An exit button is displayed at the bottom of the frame.
        self.master.clear_display()
        purchase_complete_label = tk.Label(self.master, text=f"Congratulations!\nYou have successfully purchased the number:\n\n{purchased_number}\n\nClick a button on the left to find more numbers, OR\nClick the button below to leave the program.\n", pady=15)
        purchase_complete_label.pack()
        exit_button = tk.Button(self.master, text="Exit", command=sys.exit)
        exit_button.config(width=15)
        exit_button.pack()

"""This class is called when a user starts a search."""
class Search():
    def __init__(self, search_term, display_location, available_numbers, search_frame, event=None):
        self.search_term = search_term
        self.display_location = display_location
        self.available_numbers = available_numbers
        self.search_frame = search_frame

    def show_overlong_word_message(self):
        # If the user searches for a term that is more than seven letters long, this function gives them a 
        # reminder that words above seven letters cannot have a matching 1-800 number.
        overlong_word_label = tk.Label(self.display_location, text="1-800 numbers only accommodate words up to seven letters long.\nPlease try a shorter word.")
        overlong_word_label.pack()

    def find_number_for_search_term(self):
        # Checks if there are any available numbers that match the user's word.
        if len(self.search_term) > 7:       # check that the number is short enough to be the end of a 1-800 number
            self.show_overlong_word_message()
        desired_num = wc.find_num_for_word(self.search_term)        # find the numerical ending that matches the search term
        if desired_num == "":                                       # the input is blank
            blank_input_message = tk.Label(self.display_location, text="You need to input a word to find its matching numbers.")
            blank_input_message.pack()
        else:                                                       # the user gave some input
            self.search_frame.display_desired_num(desired_num)       # tell the user what numerical ending they are looking for
            for phone_number in self.available_numbers:     # check all the available numbers for the ending
                number_found = False
                if phone_number.endswith(desired_num):
                    number_found = True
                    self.search_frame.display_search_results(phone_number)       # show the user the available number
                    break
            if number_found == False:
                self.search_frame.display_search_results(None)       # tell the user that their number is not available

"""This class displays the search window before and after the search, and instantiates the search class 
when the user submits a search term in the entry box."""
class SearchWindow():
    def __init__(self, available_numbers, master):
        self.available_numbers = available_numbers
        self.master = master

    def show_search_window(self):
        # Displays directions and a search box for the user and connects the search box with instantiating 
        # the search class.
        self.master.clear_display()
        search_directions = tk.Label(self.master, text="Enter a word here to see if it is available.\nNote: words must be 3-7 letters.")
        search_directions.pack(pady=40)
        self.search_box = tk.Entry(self.master)
        self.search_box.pack(padx=20, pady=0)
        self.search_box.focus_set()
        self.search_box.bind('<Return>', lambda event=None: self.instantiate_search(event))

    def instantiate_search(self, event=None):
        # Instantiates a search class and runs the search when the user submits a search term in the entry box
        self.clear_search_results()
        self.search = Search(self.search_box.get(), self.master, self.available_numbers, self)
        self.search.find_number_for_search_term()

    def display_desired_num(self, desired_num:str):
        # Shows the user the numerical ending that corresponds to their word. This is the numerical ending 
        # that the program is looking to match with an available phone number.
        self.desired_num_label = tk.Label(self.master, text=f"You are looking for a number ending with {desired_num}.")
        self.desired_num_label.pack()
    
    def display_search_results(self, number_results:str|None):
        # Displays the results of the search to the user. If the results are a phone number string, then it 
        # offers that phone number to the user. If the results are None, it informs the user that the number 
        # is not available.
        if number_results:      # When a phone number is returned
            search_results = tk.Label(self.master, text=f"The number you are looking for is available! It's {number_results}", fg="blue")
            search_results.pack()
            # The search results label is clickable and when clicked, it offers the number for purchase to the user.
            search_results.bind("<Button-1>", lambda event, number_results=number_results: self.master.ask_user_to_purchase(number_results))
        else:       # When return is None
            sorry_message = tk.Label(self.master, text="Sorry. That number is not available.\nTry another word, OR\nPress the button on the left to see words that are available.")
            sorry_message.pack()

    def clear_search_results(self):
        # Clears previous messages about whether or not a number is available, so that the user can make a 
        # new search.
        for i in range(len(self.master.winfo_children())-1, -1, -1):
            if i > 1:
                self.master.winfo_children()[i].destroy()

"""This window appears in the DisplayFrame when the chat button is clicked. It shows the user directions 
and a text box. When the user presses enter on the text box, ChatGPT is called to make suggestions, and 
the clickable suggestions are displayed in the display frame."""
class ChatWindow():
    def __init__(self, available_numbers, master):
        self.available_numbers = available_numbers
        self.master=master

    def show_chat_screen(self):
        # Displays the chat screen in the display frame. 
        self.master.clear_display()       # Get rid of previous display widgets
        self.chat_directions = tk.Label(self.master, pady=20, text="Write a short description of your organization.\nInclude aspects that you would like to highlight in your marketing.\nThen press enter.")
        self.chat_directions.pack()
        self.chat_box = tk.Text(self.master, wrap="word")
        self.chat_box.config(height=10, width=50)
        self.chat_box.pack()
        # an example is displayed to give the user an idea of what they might write in the box
        example_text = "Example: At Those Who Wander Travel Agency, we'll never get you lost."
        self.chat_box.insert(tk.END, example_text)      # Populate the chat box with the example text
        self.chat_box.focus_set()       # Set the focus to the chat box
        # when the user presses enter, their text is sent off to chatgpt for suggestions
        self.chat_box.bind('<Return>', lambda event=None: self.get_chat_results())

    def get_chat_results(self):
        # Calls the API on the user's input
        user_input = self.chat_box.get("1.0", "end-1c")     # Get the user's input from the text box
        api_call = APICall(user_input)      # Instantiate the APICall class
        self.display_chat_results(api_call.prepare_suggestions())       # Calls the API and displays the results

    def display_chat_results(self, suggestions:list):
        # Displays GPT's list of suggested words, along with their corresponding phone numbers and whether 
        # the phone numbers are available. All of this info is neatly formatted in columns and available 
        # numbers are clickable. If GPT does not return a list, an error message is displayed.
        self.master.clear_display()
        # Display column headers
        self.suggestions_header = tk.Label(self.master, text="ChatGPT Says:  Number:  Availability\n", font=("courier", 9))
        self.suggestions_header.pack(anchor=tk.W)
        if suggestions:     # if a list of suggestions is successfully returned
            for word in suggestions:
                if len(word) < 8:   # prevents GPT from suggesting words that are too long
                    # Check if the suggested word is available
                    available_num = wc.search_available_nums_for_word(word, self.available_numbers)
                    # Set the right formatting for available and unavailable words
                    if available_num != None:                   # when the number is available
                        availability_message = "Available!"
                        font_color = "blue"
                        cursor_assignment = "hand2"
                        available_bool = True
                    else:                                       # when the number is not available
                        availability_message = "Not available."
                        font_color = "grey"
                        cursor_assignment = "arrow"
                        available_bool = False
                    # Display available words as clickable and unavailable words as greyed out
                    label = tk.Label(self.master, text=f"{word}{' '*(15-len(word))}{wc.find_num_for_word(word)}{' '*(9-len(word))}{availability_message}", fg=font_color, font=("courier", 9), cursor=cursor_assignment)
                    label.pack(anchor=tk.W)
                    if available_bool:
                        label.bind("<Button-1>", lambda event, phone_num=available_num: self.master.ask_user_to_purchase(phone_num))
        else:               # if a list of suggestions is not returned
            self.error_label = tk.Label(self.master, text="Sorry! Something went wrong. Please try again.")
            self.error_label.pack()

"""This class shows the user a subset of the available numbers, and all the words that can be spelled 
with those numbers. This operation takes some time, so a wait message is displayed, then destroyed."""
class ShowSomeAvailableWordsWindow():
    def __init__(self, available_numbers, master):
        self.available_numbers = available_numbers
        self.master=master

    def show_some_available_words(self):
        # Finds available words and displays them as clickable labels that lead to a purchase offer window.
        self.master.clear_display()
        self.display_wait_message()
        available_combos = {}       # phone numbers will be keys and lists of words spelled from those numbers will be values
        # retrieve a subset of the available numbers. (A subset is necessary because this operation takes some time.)
        for phone_num in app.number_retrieval.get_available_phone_nums_short(self.available_numbers):
            prepared_num = wc.prepare_phone_number(phone_num)       # strip 1-800 from number
            temp_words = wc.find_words_for_num(prepared_num)        
            if temp_words:                                          # only show numbers that spell words
                temp_words.sort(key=len, reverse=True)              # show longest words on the left
                available_combos[phone_num] = temp_words
        self.directions_label = tk.Label(self.master, text="Here are some available numbers, and the words they spell.\n\nClick a number to purchase, OR\nClick Show_me_some_available_words again to see more.\n", pady=10)
        self.directions_label.pack()
        # Display all pairs of number and word list as clickable labels
        for selected_number, word_list in available_combos.items():
            label = tk.Label(self.master, text=f"{selected_number}: {[word for word in word_list]}", cursor="hand2", fg="blue")
            label.pack(anchor=tk.W)
            label.bind("<Button-1>", lambda event, offered_number=selected_number: self.master.ask_user_to_purchase(offered_number))
        self.destroy_wait_message()

    def display_wait_message(self):
        # Displays a wait message
        self.wait_message = tk.Label(self.master, text="Finding available words...")
        self.wait_message.pack()
        self.master.update()

    def destroy_wait_message(self):
        # Called when loading is finished to get rid of wait message.
        self.wait_message.destroy()
        self.master.update()


"""The display frame appears on the right side of the window and the search, chat, show, and completed 
windows appear inside of it. This class includes the formatting and geometry of those windows. It also 
has functions to clear preexisting widgets and a function to offer a phone number for purchase. These 
are functions that might be needed from any of the four windows."""
class DisplayFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=450, highlightbackground="black", highlightthickness=1)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT)

    def clear_display(self):
        # Clears all widgets from display frame, so that a new screen can appear
        leftovers = self.winfo_children()
        for widget in leftovers:
            widget.destroy()
        self.update()

    def ask_user_to_purchase(self, offered_number:str, event=None):
        # A message box appears asking the user if they want to purchase the offered_number. The user has 
        # the option to choose yes/no. If the user chooses yes, they are directed to the 'purchase complete' 
        # window. If they choose no, nothing happens.
        purchase_answer = messagebox.askyesno(f"Purchase number?", f"Do you want to purchase the number {offered_number}?")
        if purchase_answer:         # If the chooser clicks yes
            app.purchase_completion_frame.show_purchase_complete_frame(offered_number)

"""The menu frame appears on the left side of the GUI. It always displays three buttons: one for search, 
one for chat, and one for show. These buttons call the classes for the corresponding display windows."""
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

"""This class is the first to be called when the program starts. It sets the overall formatting of the 
GUI and serves as the root for the menu and display frames. It also initializes all of the classes that 
can be initialized at this point. Finally, it retrieves all of the available phone numbers, against 
which user requests can be compared."""
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set GUI format.
        self.geometry("700x400")
        self.title("1-800 Number Finder")

        # Retrieve available phone numbers to compare user requests against.
        self.number_retrieval = anf.NumberRetrieval()
        self.available_numbers_long = self.number_retrieval.get_available_phone_nums_long()

        # Initialize necessary classes.
        self.menu_frame = MenuFrame(master=self)
        self.display_frame = DisplayFrame(master=self)
        self.chat_frame = ChatWindow(self.available_numbers_long, master=self.display_frame)
        self.show_some_available_words_frame = ShowSomeAvailableWordsWindow(self.available_numbers_long, master=self.display_frame)
        self.search_frame = SearchWindow(self.available_numbers_long, master=self.display_frame)
        self.purchase_completion_frame = PurchaseCompleteWindow(master=self.display_frame)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

