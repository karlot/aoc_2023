import sys

# Part 1, simple, dummy...
def rolling_each_stone(grid):
    rgrid = [list(row) for row in list(zip(*grid))]
    for r in rgrid:
        for _ in range(len(r)):
            for ci, c in enumerate(r):
                if c == "O":
                    if ci - 1 >= 0 and r[ci - 1] == ".":
                        r[ci] = "."
                        r[ci - 1] = "O"
    return rgrid

def count_load(rgrid):
    cum1 = 0
    for r in rgrid:
        for ci, c in enumerate(reversed(r)):
            if c == "O":
                cum1 += ci + 1
    return cum1

# Part 2, better rotations, cycle detection
def cycle_nesw(grid):
    for _ in range(4):
        grid = tuple(map("".join, zip(*grid)))
        grid = tuple("#".join(["".join(sorted(tuple(group), reverse=True)) for group in row.split("#")]) for row in grid)
        grid = tuple(row[::-1] for row in grid) 
    return grid

def sum_load(grid):
    return sum(row.count("O") * (len(grid) - r) for r, row in enumerate(grid))


def main(filename):
    """
    # Results:
    Part1: 108641
    Part2: 84328
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        grid = tuple([tuple([c for c in line]) for line in lines])

    cum1 = count_load(rolling_each_stone(grid))
    print(f"Part1: {cum1}")

    # part 2 runs for 1.000.000.000 cycles, so we need to detect cycles
    cache = {grid}
    array = [grid]
    iter = 0

    while True:
        iter += 1
        grid = cycle_nesw(grid)
        if grid in cache:
            break
        cache.add(grid)
        array.append(grid)
    first = array.index(grid)
    grid = array[(1000000000 - first) % (iter - first) + first]

    print(f"Part2: {sum(row.count('O') * (len(grid) - r) for r, row in enumerate(grid))}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
