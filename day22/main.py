import sys
from collections import deque

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

    bricks = []
    max_x, max_y, max_z = 0, 0, 0
    for i, line in enumerate(lines):
        # Split lines into start and end coordinates
        x1, y1, z1, x2, y2, z2 = map(int, line.replace("~", ",").split(","))

        # Assert that initial coordinates are alway lower
        test_order = (x1 > x2) or (y1 > y2) or (z1 > z2)
        assert not test_order, f"Brick start point is larger than destination at index:{i}, {(x1, y1, z1)}-{(x2, y2, z2)}"

        bricks.append([x1, y1, z1, x2, y2, z2, i])

        # Collect info for 3D grid size
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)
        max_z = max(max_z, z1, z2)

    # Sort by hight of the brick (so we can drop from lowest point to the "grounded" level)
    sb = sorted(bricks, key=lambda b: b[2])

    # Ground level with heights
    heights = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Make the bricks fall using height-map
    settled = []
    for brick in sb:
        x1, y1, z1, x2, y2, z2, id_ = brick
        # print(f"BRICK:{id_} {(x1, y1, z1, x2, y2, z2)}")
        can_fall = True
        fall_heights = []
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                z = heights[y][x]
                if z < z1:
                    fall_heights.append(z1 - z)
                else:
                    can_fall = False
        fall = min(fall_heights) if can_fall else 0
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                # Increase height on our height-map for settled brick state
                heights[y][x] = (z1 - fall) + (z2 - z1) + 1
        settled.append((x1, y1, z1 - fall, x2, y2, z2 - fall, id_))

    # Current state of hight map (not really useful, only for settling bricks, and check settling correctness)
    # print("Height map:")
    # for y in heights:
    #     print([x - 1 for x in y])
    
    # After settling, brick can again be unordered (due to order of falling and positions)
    sb = sorted(settled, key=lambda b: b[2])
    bricks_len = len(sb)
    
    # Dictionary of which block supports which block, and gets supported by which block
    asb = {i: set() for i in range(bricks_len)}
    bsa = {i: set() for i in range(bricks_len)}

    # def overlap(a, b):
    #     return max(a[0], b[0]) <= min(a[3], b[3]) and max(a[1], b[1]) <= min(a[4], b[4])
    overlap = lambda a, b: max(a[0], b[0]) <= min(a[3], b[3]) and max(a[1], b[1]) <= min(a[4], b[4])

    # Populate support info dicts
    for j, upper in enumerate(sb):
        for i, lower in enumerate(sb[:j]):
            if overlap(lower, upper) and upper[2] == lower[5] + 1:
                asb[i].add(j)
                bsa[j].add(i)


    # Some switches when running only single part
    run_part1 = True
    run_part2 = True

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        # Count total bricks that could be removed without any bricks falling below
        # Normally this means brick is supporting some brick above, which are supported by some other brick as well
        total = 0
        for i in range(bricks_len):
            if all(len(bsa[j]) >= 2 for j in asb[i]):
                total += 1

        print(f"Part1: {total}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    if run_part2:
        # For each brick, determine how many other bricks would fall if that brick were disintegrated
        total = 0
        for i in range(bricks_len):
            q = deque(j for j in asb[i] if len(bsa[j]) == 1)
            falling = set(q)
            falling.add(i)
            while q:
                j = q.popleft()
                for k in asb[j] - falling:
                    if bsa[k] <= falling:
                        q.append(k)
                        falling.add(k)
            total += len(falling) - 1
            
        print(f"Part2: {total}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
