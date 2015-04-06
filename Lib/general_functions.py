import sys

def rindex(list, item):
    location = -1
    for index in range(len(list)-1, -1, -1):
        if item == list[index]:
            location = index
            break
    return location
