import sys
from enum import Enum

# Replacement tiles for nicer visualization
nice = {
    "|": "│",
    "-": "─",
    "F": "╭",
    "7": "╮",
    "J": "╯",
    "L": "╰",
    ".": ".",
    "S": "S",
}

# Class to nicely use direction values instead of comments
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


# Cleans map from unused pipes, and replaces them with "empty" character
# Then re-inputs only pipe path, optionally using nicer character representations
# Marks all 
def clean_map(grid, path, empty=".", use_nice=True, enclosed_char="*"):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            grid[y][x] = empty

    for px,py,char in path:
        grid[py][px] = nice[char] if use_nice else char
    
    # Process all non-loop tiles, and check if they are enclosed
    # Using ray-casting method to the right, and counting pipe-crossings.
    # If pipe-crosses are odd, then point/tile is assumed to be inside loop.
    # NOTE: This is using some assumptions for ray-offset source to above
    #       "middle" of char-field, to correctly count crosses.
    enclosed = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if grid[y][x] == empty:
                crosses = 0
                for i in range(x, len(grid[y])):
                    charset = ["╯", "╰", "│"] if use_nice else ["J", "L", "|"]
                    if grid[y][i] in charset:
                        crosses += 1
                
                # Check if checked tile is "enveloped"
                if crosses % 2 == 1:
                    grid[y][x] = enclosed_char
                    enclosed += 1
    return enclosed


# Helpers since used more than once
def check_up(grid, x, y):
    return grid[y-1][x] in ["F", "|", "7"]

def check_right(grid, x, y):
    return grid[y][x+1] in ["7", "-", "J"]

def check_down(grid, x, y):
    return grid[y+1][x] in ["L", "|", "J"]

def check_left(grid, x, y):
    return grid[y][x-1] in ["F", "-", "L"]


# Mainly used to find original pipe for starting point
def find_connection(grid, x, y):
    if check_up(grid, x, y)   and check_down(grid, x, y):  return "|"
    if check_left(grid, x, y) and check_right(grid, x, y): return "-"
    if check_up(grid, x, y)   and check_right(grid, x, y): return "L"
    if check_up(grid, x, y)   and check_left(grid, x, y):  return "J"
    if check_down(grid, x, y) and check_left(grid, x, y):  return "7"
    if check_down(grid, x, y) and check_right(grid, x, y): return "F"
    assert 0, "Unreachable!"

            
# Gets location of Animal starting point
def find_animal(grid, replace=True):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "S":
                # Replace "animal" character with correct pipe info
                if replace:
                    # print(find_connection(grid, x, y))
                    real_tile = find_connection(grid, x, y)
                    grid[y][x] = real_tile
                    return (x, y, real_tile)
                return (x, y, "S")
    assert 0, "Unreachable!"


def check_next(grid, x, y, direction=None):
    if direction == None:
        if check_up(grid, x, y):    return x, y-1, Direction.UP
        if check_right(grid, x, y): return x+1, y, Direction.RIGHT
        if check_down(grid, x, y):  return x, y+1, Direction.DOWN
        if check_left(grid, x, y):  return x-1, y, Direction.LEFT
        assert 0, "Unreachable!"

    # Current position
    cp = grid[y][x]
    match direction:
        case Direction.UP:
            if cp == "F": return x+1, y, Direction.RIGHT
            if cp == "|": return x, y-1, Direction.UP
            if cp == "7": return x-1, y, Direction.LEFT
        case Direction.RIGHT:
            if cp == "7": return x, y+1, Direction.DOWN
            if cp == "-": return x+1, y, Direction.RIGHT
            if cp == "J": return x, y-1, Direction.UP
        case Direction.DOWN:
            if cp == "L": return x+1, y, Direction.RIGHT
            if cp == "|": return x, y+1, Direction.DOWN
            if cp == "J": return x-1, y, Direction.LEFT
        case Direction.LEFT:
            if cp == "F": return x, y+1, Direction.DOWN
            if cp == "-": return x-1, y, Direction.LEFT
            if cp == "L": return x, y-1, Direction.UP
    assert 0, "Unreachable!"


def main(filename):
    """
    # Results:
    Part1: 6828
    Part2: 459
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    # Convert to grid
    grid = [[char for char in line.strip()] for line in lines]

    ax, ay, rt = find_animal(grid, replace=True)
    nx, ny = 0, 0
    direction = None
    total_step = 0

    main_path = [(ax,ay, rt)]
    while True:
        if direction:
            nx, ny, direction = check_next(grid, nx, ny, direction)
        else:
            print(f"Start: {ax=} {ay=}")
            nx, ny, direction = check_next(grid, ax, ay, None)

        # print(f"Next location: {nx=}, {ny=}, {direction=}")
        total_step += 1
        if nx == ax and ny == ay:
            break
        main_path.append((nx, ny, grid[ny][nx]))

    # Print simplified map
    enclosed = clean_map(grid, main_path, use_nice=True)
    for r in grid:
        for c in r:
            print(c, end="")
        print()
    
    print(f"Part1: {total_step // 2}")
    print(f"Part2: {enclosed}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
