"""This module stores the logic to do the underlying work of preparing phone numbers and checking for 
matches with English words.
"""

from itertools import product
import enchant

# A dictionary against which to check whether derived words are English words
word_list = enchant.Dict("en_US")
# The keyboard of a phone, with letters assigned to different digits
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
# The keyboard of a phone, this time with numbers included
letter_assignments_plus_nums = {
    '0':['0'], 
    '1':['1'],
    '2':['a', 'b', 'c', '2'], 
    '3':['d', 'e', 'f', '3'], 
    '4':['g', 'h', 'i', '4'], 
    '5':['j', 'k', 'l', '5'], 
    '6':['m', 'n', 'o', '6'], 
    '7':['p', 'q', 'r', 's', '7'], 
    '8':['t', 'u', 'v', '8'], 
    '9':['w', 'x', 'y', 'z', '9']
}

# Throws an exception when the input is not a valid phone number.
class InvalidPhoneNumberError(Exception):
    def __init__(self, message="The input is not a valid phone number"):
        self.message = message
        super().__init__(self.message)
        self.message = message

def prepare_phone_number(phone_num : str) -> list[str]:
    # Strips 1-800 or 800 off of the input and makes sure that it is a valid number. 
    # Then returns number as a list of digit strings
    if type(phone_num) == str:
        if len(phone_num) == 11:
            shortened_num = phone_num[4:]
            digit_list = [num for num in shortened_num]
        else:   # when the phone_num is too long or short
            raise InvalidPhoneNumberError
    else:   # when the phone_num is not a string
        raise InvalidPhoneNumberError
    return digit_list

def find_words_for_num(phone_num : list[str]) -> list[str]:
    # Takes a phone number in the form of a list of digit strings.  
    # Outputs a list of words that can be spelled using that phone number.

    words = product(*(letter_assignments[digit] for digit in phone_num))
    
    solution_words = []

    for word in words:
        word = ''.join(word)
        for i in range(0, 5):
            if word_list.check(word[i:]) == True:
                if word[i:] not in solution_words:
                    solution_words.append(word[i:])
        
    return solution_words

def find_num_for_word(word : str) -> str:
    # Takes a desired word and returns the string of digits that spell it. Returns an empty string if passed 
    # an empty string. 
    letter_list = [letter for letter in word.lower()]
    digit_list = []
    for letter in letter_list:
        for key, value in letter_assignments_plus_nums.items():
            for num in value:
                if num == letter:
                    digit_list.append(key)
    phone_num = ''.join(digit_list)
    return phone_num

def search_available_nums_for_word(word : str, available_nums : list[str]) -> str|None:
    # Given a desired word and a list of available numbers, this function outputs the number that 
    # spells the desired word. The number is in the form of a string. If the word is not available, the
    # function will return None.
    needed_num = find_num_for_word(word)
    for digit_list in available_nums:
        digit_str = ''.join(digit_list)
        if digit_str.endswith(needed_num):
            return digit_list
    return None

