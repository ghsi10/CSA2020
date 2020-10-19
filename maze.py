from pwn import *

sys.setrecursionlimit(2 ** (struct.Struct('i').size * 8 - 1) - 1)


def get_input():
    output = ""
    while "What is your command?" not in output:
        output += p.recvline()
    return output.replace("> What is your command?", "").replace("\n", "").replace("\xe2", "V").strip()


def go(step):
    p.send(step)
    answer = get_input()
    if answer != "1" and answer != "0":
        print(answer)
    if "1" in answer:
        return True
    return False


num_of_points = 6


def scan(y, x):
    if y < 0 or y > 250 or x < 0 or x > 250:
        return
    if maze[y][x] > 0 or len(dl) >= num_of_points:
        return
    maze[y][x] = 1
    p.send("g")
    output = get_input()
    if output != "far far away":
        d = output.split(" ")[-1]
        p.send("c")
        location = get_input()
        print(location, d)
        dl.append((location, d))
    if go("l"):
        scan(y, x - 1)
        if len(dl) < num_of_points:
            go("r")
    if go("d"):
        scan(y - 1, x)
        if len(dl) < num_of_points:
            go("u")
    if go("r"):
        scan(y, x + 1)
        if len(dl) < num_of_points:
            go("l")
    if go("u"):
        scan(y + 1, x)
        if len(dl) < num_of_points:
            go("d")


maze = [[0 for i in range(251)] for j in range(251)]
p = remote("maze.csa-challenge.com", 80)

start_x = 0
start_y = 0
output = ""
dl = []
while "What is your command?" not in output:
    output = p.recvline().decode()
    if "(" in output:
        start_x, start_y = output.split("(")[1][:-2].split(",")
print("start:")
print(start_x, start_y)
print("***********")
scan(int(start_y), int(start_x))
p.interactive()

