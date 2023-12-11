import sys
# import re
# from collections import defaultdict

def find_animal(lines):
    animal = None
    for y, line in enumerate(lines):
        try:
            x = line.index("S") 
        except:
            continue
        animal = (x, y)
        break
    return animal


def check_next(lines, x, y, d):
    cp = lines[y][x]
    if d == None:
        # Going UP
        if lines[y-1][x] in ["F", "|", "7"]:
            return x, y-1, 1
        # Going RIGHT
        if lines[y][x+1] in ["7", "-", "J"]:
            return x+1, y, 2
        # Going DOWN
        if lines[y+1][x] in ["L", "|", "J"]:
            return x, y+1, 3
        # Going LEFT
        if lines[y][x-1] in ["F", "-", "L"]:
            return x-1, y, 4
        # UNREACHABLE
        assert 0, "Unexpected!"

    # Up
    if d == 1:
        if cp == "F":
            # turn right
            return x+1, y, 2
        if cp == "|":
            # continue up
            return x, y-1, 1
        if cp == "7":
            # turn left
            return x-1, y, 4
    # Right
    if d == 2:
        if cp == "7":
            # turn down
            return x, y+1, 3
        if cp == "-":
            # continue right
            return x+1, y, 2
        if cp == "J":
            # turn up
            return x, y-1, 1
    # Down
    if d == 3:
        if cp == "L":
            # turn right
            return x+1, y, 2
        if cp == "|":
            # continue down
            return x, y+1, 3
        if cp == "J":
            # turn left
            return x-1, y, 4
    # Left
    if d == 4:
        if cp == "F":
            # turn down
            return x, y+1, 3
        if cp == "-":
            # continue left
            return x-1, y, 4
        if cp == "L":
            # turn up
            return x, y-1, 1
    assert 0, "Unexpected!"


def main(filename):
    """
    # Results:
    """
    with open(filename, "r") as f:
        lines = f.readlines()
    
    ax, ay = find_animal(lines)
    nx, ny = 0, 0
    direction = None
    total_step = 0

    while True:
        if direction:
            nx, ny, direction = check_next(lines, nx, ny, direction)
        else:
            print(f"Start: {ax=} {ay=}")
            nx, ny, direction = check_next(lines, ax, ay, None)

        # print(f"Next location: {nx=}, {ny=}, {direction=}")
        total_step += 1
        if nx == ax and ny == ay:
            break


    print(f"Part1: {int(total_step/2)}")
    print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])