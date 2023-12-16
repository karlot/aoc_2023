import sys
from collections import deque

def calculate(r, c, dr, dc, grid):
    a = [(r, c, dr, dc)]
    seen = set()
    q = deque(a)

    while q:
        r, c, dr, dc = q.popleft()
        r += dr
        c += dc

        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]): continue

        ch = grid[r][c]
        if ch == "." or (ch == "-" and dc != 0) or (ch == "|" and dr != 0):
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        elif ch == "/":
            dr, dc = -dc, -dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        elif ch == "\\":
            dr, dc = dc, dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        else:
            for dr, dc in [(1, 0), (-1, 0)] if ch == "|" else [(0, 1), (0, -1)]:
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))
                    
    coords = {(r, c) for (r, c, _, _) in seen}
    return len(coords)


# Find one path, from top-left position towards right
def part1(grid):
    return calculate(0, -1, 0, 1, grid)


# Find all possible paths
def part2(grid):
    max_val = 0
    for r in range(len(grid)):
        max_val = max(max_val, calculate(r, -1, 0, 1, grid))
        max_val = max(max_val, calculate(r, len(grid[0]), 0, -1, grid))
    for c in range(len(grid)):
        max_val = max(max_val, calculate(-1, c, 1, 0, grid))
        max_val = max(max_val, calculate(len(grid), c, -1, 0, grid))
    return max_val
    

def main(filename):
    """
    # Results:
    Part1: 8125
    Part2: 8489
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        grid = tuple([tuple([c for c in line]) for line in lines])


    print(f"Part1: {part1(grid)}")
    print(f"Part2: {part2(grid)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
