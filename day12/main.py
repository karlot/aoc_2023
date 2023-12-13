import sys


def main(filename):
    """
    # Results:
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    print(f"Part1: {None}")
    print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
