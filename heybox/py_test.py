import time
import random
import math

list1 = [99, 22, 11]
list2 = [9, 88, 19]

# print(list1 + list2)


def get_random_number():
    print('start rolling')
    time.sleep(2)
    result = random.random() * 10
    result = round(result, 2)
    print('number out ! {}'.format(result))
    return result


# get_random_number()
# get_random_number()
print(round(2.5))
