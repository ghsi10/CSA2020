import string
import math


printable = string.printable

with open('./hops.txt') as f:
    iter_sort = f.read().split('\n')

for i in range(len(iter_sort)):
    iter_sort[i] = iter_sort[i].split(" ")[1:]
    iter_sort[i] = list(map(int, iter_sort[i]))

# change_sort = sorted(iter_sort, key=lambda x: x[1])

input_dict = {}
for hop in iter_sort:
    i = hop[1]
    if i in input_dict.keys():
        input_dict[i].append(hop)
    else:
        input_dict[i] = [hop]



final_flag = []
for i in range(40):
    possabilities = []
    for ch in printable:
        letter = ord(ch)
        is_possible = True
        for change in input_dict[i]:
            right_if = bool(4 - change[0])
            mod_bool = letter % change[2]
            left_if = mod_bool == 0
            do_not_true_me = left_if == right_if
            if do_not_true_me:
                is_possible = False
                break
            if not mod_bool:
                letter = math.floor(letter / change[2])
        if is_possible:
            possabilities.append(ch)
    final_flag.append(possabilities)

# print(final_flag)
flag = ""
for possability in final_flag:
    for p in possability:
        flag += p

print(flag)