"""This program simulates finding available 1-800 phone numbers, by making numbers up. It 
can make up a short run of phone numbers, or a long run for different purposes.
"""

import random

class NumberRetrieval():
    def __init__(self):

        self.SHORT_RUN = 20
        self.LONG_RUN = 20000

    # Nerfed: Will retrieve available phone numbers and return them as a list of strings. 
    def get_available_phone_nums_short(self) -> list[str]:
        available_phone_nums = []
        for i in range(self.SHORT_RUN):
            available_phone_nums.append(str(random.randint(18000000000, 18009999999)))
        return available_phone_nums

    def get_available_phone_nums_long(self) -> list[str]:
        available_phone_nums = []
        for i in range(self.LONG_RUN):
            available_phone_nums.append(str(random.randint(18000000000, 18009999999)))
        return available_phone_nums

if __name__ == "__main__":
    test_instance = NumberRetrieval()
    print(test_instance.get_available_phone_nums_long())