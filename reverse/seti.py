import re

signal1 = None
with open('second_signal.txt', 'r') as file:
    signal1 = eval(file.read())

for one_char in signal1:
    regexs = []
    for array in one_char:
        regex = ""
        for x in array:
            regex += f".*[{x}]"
        regex += ".*"
        regexs.append(regex)

    letters = []
    for i in range(33,126):
        num = str(bin(i))[2:].rjust(8, "0")
        is_match = True
        for reg in regexs:
            if not re.compile(reg).match(num):
                is_match = False
        if is_match:
            letters.append(chr(i))
    print(letters)
