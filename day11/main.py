import sys


# Finds and marks empty rows and columns
def mark_empty(grid):
    empty_rows = []
    for i in range(len(grid)):
        if all([tile != "#" for tile in grid[i]]):
            empty_rows.append(i)

    empty_cols = []
    cgrid = list(map(list, zip(*grid)))
    for i in range(len(cgrid)):
        if all([tile != "#" for tile in cgrid[i]]):
            empty_cols.append(i)
    return list(map(list, zip(*cgrid))), empty_rows, empty_cols


# Calculates total distances between galaxies, based on empty space "width"
def calc_total_dist(lines, mul):
    grid = [[1 if c == "." else "#" for c in row.strip()] for row in lines]
    grid, empty_rows, empty_cols = mark_empty(grid)

    gid = 1
    galaxies = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                galaxies.append((gid, r, c))
                gid += 1

    done = {}
    for sid, sr, sc in galaxies:
        for did, dr, dc in galaxies:
            if sid == did: continue
            q1 = f"{sid}:{did}"
            q2 = f"{did}:{sid}"
            if q1 in done or q2 in done: continue

            cum = abs(sr - dr) + abs(sc - dc)
            
            for r in empty_rows:
                if min(sr, dr) <= r <= max(sr, dr):
                    cum += mul-1
            for c in empty_cols:
                if min(sc, dc) <= c <= max(sc, dc):
                    cum += mul-1

            done[q1] = cum
            done[q2] = 0
    
    total_distances = sum(done.values())
    return total_distances


def main(filename):
    """
    # Results:
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    print(f"Part1: {calc_total_dist(lines, 2)}")
    print(f"Part2: {calc_total_dist(lines, 1000000)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
