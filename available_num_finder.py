
import random

SHORT_RUN = 20
LONG_RUN = 50

# Nerfed: Will retrieve available phone numbers and return them as a list of strings. 
def get_available_phone_nums_short() -> list[str]:
    available_phone_nums = []
    for i in range(SHORT_RUN):
        available_phone_nums.append(str(random.randint(18000000000, 18009999999)))
    return available_phone_nums

def get_available_phone_nums_long() -> list[str]:
    available_phone_nums = []
    for i in range(LONG_RUN):
        available_phone_nums.append(str(random.randint(18000000000, 18009999999)))
    return available_phone_nums

if __name__ == "__main__":
    print(get_available_phone_nums())