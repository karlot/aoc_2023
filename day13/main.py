import sys

def check_mirrored(p, part):
    for r in range(1, len(p)):
        if part == 1:
            if p[:r][::-1][:len(p[r:])] == p[r:][:len(p[:r][::-1])]: return r
        else:
            if sum(sum(0 if a == b else 1 for a, b in zip(x, y)) for x, y in zip(p[:r][::-1], p[r:])) == 1: return r
    return 0

def main(filename):
    """
    # Results:
    Part1: 33735
    Part2: 38063
    """
    with open(filename) as f:
        patterns = [part.splitlines() for part in f.read().split("\n\n")]
    
    cumulated = [0, 0, 0]
    for p in patterns:
        for part in [1, 2]:
            cumulated[part] += check_mirrored(p, part) * 100
            cumulated[part] += check_mirrored(list(zip(*p)), part)
    
    print(f"Part1: {cumulated[1]}")
    print(f"Part2: {cumulated[2]}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
