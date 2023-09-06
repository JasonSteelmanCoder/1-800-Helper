import available_num_finder as anf
import word_checker as wc
import tkinter as tk

def show_search_window():
    global search_box
    word_search_window = tk.Toplevel()
    search_directions = tk.Label(word_search_window, text="Enter a word here to see if it is available.\nNote: words must be 3-7 letters.")
    search_directions.pack()
    search_box = tk.Entry(word_search_window)
    search_box.pack(padx=20, pady=20)
    search_box.focus_set()
    search_box.bind('<Return>', find_word_for_input)

# TODO: handle the return from this function. If it returns None, tell the user the num is not available;
# if it returns the number, say 'Congratulations! Your number is available!'
def find_word_for_input(event=None):
    global search_box
    user_input = search_box.get()
    desired_num = wc.find_num_for_word(user_input)
    for phone_number in anf.get_available_phone_nums():
        if phone_number.endswith(desired_num):
            return phone_number
    return None

def show_available():
    show_available_window = tk.Toplevel()
    available_combos = {}
    for num in anf.get_available_phone_nums():
        prepared_num = wc.prepare_phone_number(num)
        temp_words = wc.find_words_for_num(prepared_num)
        if temp_words:
            temp_words.sort(key=len, reverse=True)
            available_combos[num] = temp_words
    formatted_output = format_output(available_combos)
    available_combos_label = tk.Label(show_available_window, text=formatted_output, justify=tk.LEFT)
    available_combos_label.pack(pady=20)

def format_output(combos:dict) -> str:
    combo_list = []
    for item in combos.items():
        combo_list.append(str(item))
    combo_list.sort(key=len, reverse=True)
    combo_str = "\n".join(combo_list)
    return combo_str

root = tk.Tk()

label = tk.Label(root, text="Chose what you want to do.")
label.pack(pady=20)

find_num_button = tk.Button(root, text="Check if my word is available.", command=show_search_window)
find_num_button.pack(pady=20)

find_word_button = tk.Button(root, text="Let me choose an available word.", command=show_available)
find_word_button.pack(pady=20)

root.mainloop()

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
