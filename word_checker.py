"""When someone has a 1-800 number, they often advertise it using a word. For example, 1-800-222-PAIN.
The word is made using the letters that would appear on a number pad for the digits in the phone number.

This program is meant to help a person who is choosing an available 1-800 number for their company.
It will take a phone number as an input and find all of the words that can be spelled with those digits."""

import enchant

word_list = enchant.Dict("en_US")
letter_assignments = {
    '0':[], 
    '1':[],
    '2':['a', 'b', 'c'], 
    '3':['d', 'e', 'f'], 
    '4':['g', 'h', 'i'], 
    '5':['j', 'k', 'l'], 
    '6':['m', 'n', 'o'], 
    '7':['p', 'q', 'r', 's'], 
    '8':['t', 'u', 'v'], 
    '9':['w', 'x', 'y', 'z']
}

# Throws an exception when the input is not a valid phone number.
class InvalidPhoneNumber(Exception):
    def __init__(self, message="The input is not a valid phone number"):
        super().__init__()
        self.message = message

# Strips 1-800 or 800 off of the input and makes sure that it is a valid number. 
# Then returns number as a list of digit strings
def prepare_phone_number(phone_num : str) -> list[str]:
    if type(phone_num) == str:
        if len(phone_num) == 11:
            shortened_num = phone_num[4:]
            digit_list = [num for num in shortened_num]
        else:   # when the phone_num is too long or short
            raise InvalidPhoneNumber
    else:   # when the phone_num is not a string
        raise InvalidPhoneNumber
    return digit_list

# Takes a phone number in the form of a list of digit strings.  
# Outputs a list of words that can be spelled using that phone number.
def find_words_for_num(phone_num : list[str]) -> list[str]:
    letters_list = []
    for digit in phone_num:
        if digit == '0':
            letters_list.append([digit])
        elif digit == '1':
            letters_list.append([digit])
        else:   # when the digit has letters assigned to it
            key_letters = letter_assignments[digit]
            letters_list.append(key_letters)
    letter_lists = []
    for letter0 in letters_list[0]:
        for letter1 in letters_list[1]:
            for letter2 in letters_list[2]:
                for letter3 in letters_list[3]:
                    for letter4 in letters_list[4]:
                        for letter5 in letters_list[5]:
                            for letter6 in letters_list[6]: 
                                potential_word = []
                                potential_word.append(letter0)
                                potential_word.append(letter1)
                                potential_word.append(letter2)
                                potential_word.append(letter3)
                                potential_word.append(letter4)
                                potential_word.append(letter5)
                                potential_word.append(letter6)
                                letter_lists.append(potential_word)
    
    words = []
    for letter_list in letter_lists:
        words.append(''.join(letter_list))
    
    solution_words = []

    for word in words:
        if word_list.check(word) == True:
            solution_words.append(word)
    
    shortened_words = []
    for word in words:
        shortened_words.append(word[1:])
        shortened_words.append(word[2:])
        shortened_words.append(word[3:])
        shortened_words.append(word[4:])

    for word in shortened_words:
        if word_list.check(word) == True:
            if word not in solution_words:
                solution_words.append(word)

    return solution_words

# Takes a desired word and returns the string of digits that spell it.
def find_num_for_word(word : str) -> str:
    letter_list = [letter for letter in word]
    digit_list = []
    for letter in letter_list:
        for key, value in letter_assignments.items():
            for num in value:
                if num == letter:
                    digit_list.append(key)
    phone_num = ''.join(digit_list)
    return phone_num

# Given a desired word and a list of available numbers, this function outputs the number that 
# spells the desired word. The number is in the form of a string. If the word is not available, the
# function will return None.
def search_available_nums_for_word(word : str, available_nums : list[str]) -> str:
    needed_num = find_num_for_word(word)
    for digit_list in available_nums:
        digit_str = ''.join(digit_list)
        if needed_num in digit_str:
            return digit_list
        else:   # when the word cannot be made by the available numbers
            return None

# TODO:
# - make nice clean function calls, possibly in another module
# - write unit tests
# - clean up testing print statements
# - add a GUI
# - look into how to actually find available 1-800 numbers
# - tidy the find_available_numbers module