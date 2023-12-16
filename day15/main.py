import sys

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
        grid = tuple([tuple([c for c in line]) for line in lines])

    print(f"Part1: {None}")
    print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
