import available_num_finder as anf
import word_checker as wc
import tkinter as tk

def find_word_for_input(event=None):
    global search_box
    user_input = search_box.get()
    desired_num = wc.find_num_for_word(user_input)
    for phone_number in anf.get_available_phone_nums():
        if phone_number.endswith(desired_num):
            return phone_number
    return None

def format_output(combos:dict) -> str:
    combo_list = []
    for item in combos.items():
        combo_list.append(str(item))
    combo_list.sort(key=len, reverse=True)
    combo_str = "\n".join(combo_list)
    return combo_str

def clear_display():
    leftovers = app.display_frame.winfo_children()
    for widget in leftovers:
        widget.destroy()
    app.display_frame.update()

def display_wait_message():
    app.display_frame.wait_message = tk.Label(app.display_frame, text="Finding available words...")
    app.display_frame.wait_message.pack()
    app.display_frame.update()

def destroy_wait_message():
    app.display_frame.wait_message.destroy()
    app.display_frame.update()

def show_available():
    clear_display()
    display_wait_message()
    available_combos = {}
    for num in anf.get_available_phone_nums():
        prepared_num = wc.prepare_phone_number(num)
        temp_words = wc.find_words_for_num(prepared_num)
        if temp_words:
            temp_words.sort(key=len, reverse=True)
            available_combos[num] = temp_words
    formatted_output = format_output(available_combos)
    available_combos_label = tk.Label(app.display_frame, text=formatted_output, justify=tk.LEFT)
    available_combos_label.pack(pady=20)
    destroy_wait_message()

def show_search_window():
    clear_display()
    search_directions = tk.Label(app.display_frame, text="Enter a word here to see if it is available.\nNote: words must be 3-7 letters.")
    search_directions.pack(pady=40)
    search_box = tk.Entry(app.display_frame)
    search_box.pack(padx=20, pady=0)
    search_box.focus_set()
    search_box.bind('<Return>', find_word_for_input)

class DisplayFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.configure(height=400, width=450, highlightbackground="black", highlightthickness=1)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT)

class MenuFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.configure(height=400, width=250, bg="#4287f5")
        self.pack_propagate(False)
        self.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Chose what you want to do:", bg="#4287f5")
        self.label.pack(pady=50)

        self.find_num_button = tk.Button(self, text="Check if my word is available.", command=show_search_window)
        self.find_num_button.pack(pady=20)

        self.find_word_button = tk.Button(self, text="Let me choose an available word.", command=show_available)
        self.find_word_button.pack(pady=30)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("1-800 Number Finder")

        self.menu_frame = MenuFrame()
        self.display_frame = DisplayFrame()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# TODO:
# - handle the return from find_word_for_input. 
#       If it returns None, tell the user the num is not available;
#       if it returns the number, say 'Congratulations! Your number is available!'
# - show available numbers while available words are loading
# - move functions inside display frame
# - clean up the comments
# - write unit tests
# - make other modules OOP



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
