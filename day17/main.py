import sys
from queue import PriorityQueue

def solve_hl(grid, min_forward, max_forward):
    # Grid size
    max_rows = len(grid)
    max_cols = len(grid[0])

    # Need to keep track of node locations that we already passed
    checked = {
        (0, 0, 0, 1, 0): 0,
        (0, 0, 1, 0, 0): 0,
    }

    # Our destination position
    destination = (max_rows - 1, max_cols - 1)

    # For Dijkstra we need priority queue
    # Init with two options to move from our starting position in top-left corner: move right and down
    pq = PriorityQueue()
    pq.put((0, 0, 0, 0, 1, 0))  # try right +1
    pq.put((0, 0, 0, 1, 0, 0))  # try down  +1

    result = None
    while not pq.empty():
        # Get from priority queue item with lowest value (smallest cost/heat-loss)
        hl, r, c, dr, dc, steps = pq.get()
        if (r, c) == destination:
            result = hl
            break

        # Make check if we have been here, and if yes, move to next item in queue
        checkpoint = (r, c, dr, dc, steps)
        if hl > checked[checkpoint]:
            continue

        # Save checkpoint location with known heat-loss
        # checked[checkpoint] = heat_loss
        directions = []

        if steps < max_forward:
            directions.append((dr, dc))

        if steps >= min_forward: 
            directions.append((-dc, dr))
            directions.append((dc, -dr))

        for ndr, ndc in directions:
            nr = r + ndr
            nc = c + ndc
            if 0 <= nr < max_rows and 0 <= nc < max_cols:
                nhl = hl + grid[nr][nc]
                checkpoint = (nr, nc, ndr, ndc, steps + 1 if (ndr, ndc) == (dr, dc) else 1)

                if checkpoint not in checked or nhl < checked[checkpoint]:
                    checked[checkpoint] = nhl
                    pq.put((nhl, *checkpoint))
    return result


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
        grid = tuple([tuple([int(c) for c in line]) for line in lines])

    print(f"Part1: {solve_hl(grid, 0, 3)}")
    print(f"Part2: {solve_hl(grid, 4, 10)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
