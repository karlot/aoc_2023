import sys
import re


def process_path(lines, part):
    path = []
    x, y = 0, 0
    min_x, min_y = 0, 0
    max_x, max_y = 0, 0

    for line in lines:
        d, m, c = re.match(r"([UDRL]) (\d+) \(#(\w+)\)", line).groups()
        if part ==  2:
            m = int(c[0:5], 16)
            d = ("R", "D", "L", "U")[int(c[5])]
            print(d, m)
        m = int(m)
        match d:
            case "U":
                y -= m
                if y < min_y: min_y = y
            case "D":
                y += m
                if y > max_y: max_y = y
            case "L":
                x -= m
                if x < min_x: min_x = x
            case "R":
                x += m
                if x > max_x: max_x = x
            case _:   assert 1, "Unexpected direction!"
        path.append((d, m, c))
        # print((x, y), (min_x, max_x, min_y, max_y))

    gy = abs(min_y) + max_y + 1
    gx = abs(min_x) + max_x + 1
    return path, gx, gy, min_x, min_y


def dig_lagoon(path, gx, gy, ox, oy):
    grid = [["." for _ in range(gx)] for _ in range(gy)]
    x, y = abs(ox), abs(oy)
    # print(f"Starting point: {x=}, {y=}")

    trench_volume = 0
    for d, m, c in path:
        # print(f"Point: {x=}, {y=}, going: {d=} {m=} times")
        trench_volume += m
        match d:
            case "U":
                for _ in range(m):
                    y -= 1
                    grid[y][x] = "#"
            case "D":
                for _ in range(m):
                    y += 1
                    grid[y][x] = "#"
            case "L":
                for _ in range(m):
                    x -= 1
                    grid[y][x] = "#"
            case "R":
                for _ in range(m):
                    x += 1
                    grid[y][x] = "#"

    # Dimensions
    rows, cols = len(grid), len(grid[0])

    # Flood fill
    def flood_fill(matrix, y, x):
        stack = [(y, x)]
        flooded = 0

        while stack:
            y, x = stack.pop()
            if 0 <= y < rows and 0 <= x < cols and matrix[y][x] == ".":
                matrix[y][x] = "#"
                flooded += 1

                # Add neighbors to the stack
                stack.append((y + 1, x))
                stack.append((y - 1, x))
                stack.append((y, x + 1))
                stack.append((y, x - 1))
        
        return flooded

    # Find starting point for fill (somewhere inside)
    start_x, start_y = 0, 0
    for y, r in enumerate(grid):
        found = False
        for x, c in enumerate(r):
            if y == 0 or x == 0: continue
            if x == cols - 1: continue
            if c == "#" and grid[y][x-1] == "." and grid[y][x+1] == ".":
                start_x = x + 1
                start_y = y
                found = True
                # print(f"Found inside point: {start_x=} {start_y=}")
                break
        if found:
            break

    # Dig inside trench
    total_volume = flood_fill(grid, start_y, start_x) + trench_volume
    return total_volume, grid


def main(filename):
    """
    # Results:
    Part1: 
    Part2: 
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        # grid = tuple([tuple([c for c in line]) for line in lines])

    part1, _ = dig_lagoon(*process_path(lines, 1))
    # part2, _ = dig_lagoon(*process_path(lines, 2))    ## does not work, eats all the memory

    print(f"Part1: {part1}")
    print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
