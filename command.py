import available_num_finder as anf
import word_checker as wc
import tkinter as tk

class Search():
    def __init__(self, search_term, event=None):
        self.search_term = search_term

    def find_word_for_search_term(self):
        app.display_frame.clear_search_results()
        desired_num = wc.find_num_for_word(self.search_term)

        app.display_frame.desired_num_label = tk.Label(app.display_frame, text=f"You are looking for a number ending with {desired_num}.")
        app.display_frame.desired_num_label.pack()
        
        for phone_number in anf.get_available_phone_nums():
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
        for num in anf.get_available_phone_nums():
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
            print("creating sorry message.")

    def clear_search_results(self):
        for i in range(len(self.winfo_children())-1, -1, -1):
            if i > 1:
                self.winfo_children()[i].destroy()

class MenuFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.configure(height=400, width=250, bg="#4287f5")
        self.pack_propagate(False)
        self.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Chose what you want to do:", bg="#4287f5")
        self.label.pack(pady=50)

        self.find_num_button = tk.Button(self, text="Check if my word is available.", command=lambda: app.display_frame.show_search_window())
        self.find_num_button.pack(pady=20)

        self.find_word_button = tk.Button(self, text="Let me choose an available word.", command=lambda: app.display_frame.show_available_words())
        self.find_word_button.pack(pady=30)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("1-800 Number Finder")

        self.menu_frame = MenuFrame(master=self)
        self.display_frame = DisplayFrame(master=self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# TODO:
# - add further directions when your word is not available (like look at the available nums)
# - add error handling for when users put in numbers that are too long, wrong type, etc.
# - clean up display format for list of available numbers
# - stop looking for 3 letter words and get a larger number of words from anf
# - change anf (and its caller) so that it makes more numbers when you are looking for a specific word
# - fix the InvalidPhoneNumber exception in word_checker.py
# - make other modules OOP
# - write unit tests
# - clean up the comments
# - add docstrings for each function



# TESTING CALLS:
# print(anf.get_available_phone_nums())
# print(wc.find_num_for_word('pain'))
# print(wc.prepare_phone_number('18001234567'))

# available_nums_w_pain = [['9', '9', '9', '7', '2', '4', '6']]
# available_nums_without_pain = [['9', '9', '9', '9', '9', '9', '9'], ['1', '2', '3', '4', '5', '6', '7']]
# print(wc.search_available_nums_for_word('pain', available_nums_w_pain))
# print(wc.search_available_nums_for_word('pain', available_nums_without_pain))

# print(wc.find_words_for_num(['9', '4', '6', '4', '2', '7', '6']))
#   Should yield ['zingaro', 'arm', 'bpm', 'bro', 'harm', 'micro']

# for phone_num in anf.get_available_phone_nums():
#     print(wc.find_words(wc.prepare_phone_number(phone_num)))
