import sys

# Hash function
# -------------
# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.
def myhash(input_str):
    val = 0
    for c in input_str:
        val = ((val + ord(c)) * 17) % 256
    return val


def main(filename):
    """
    # Results:
    Part1: 505427
    Part2: 243747
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        grid = tuple([tuple([c for c in line]) for line in lines])

    opcodes = lines[0]

    print(f"Part1: {sum(map(myhash, opcodes.split(',')))}")

    # Make 256 "boxes", and store focal-lengths for each lens
    boxes = [[] for _ in range(256)]
    focal_lengths = {}

    for opcode in opcodes.split(","):
        if opcode[-1] == "-":
            label = opcode[:-1]
            index = myhash(label)
            if label in boxes[index]: boxes[index].remove(label)
        else:
            label, f_length = opcode.split("=")
            index = myhash(label)
            if label not in boxes[index]: boxes[index].append(label)
            focal_lengths[label] = int(f_length)

    total = 0
    for bi, box in enumerate(boxes, 1):
        for li, label in enumerate(box, 1):
            total += bi * li * focal_lengths[label]

    print(f"Part2: {total}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
