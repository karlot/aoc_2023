import sys

# Since initial alg was not possible to complete with part2...
# Try #2: recursive calculation processing algorithm by segments
# Try #3: Still slow, adding cache
cache = {}
def record_score(record, info):
    # Edge cases...
    if record == "": return 1 if info == () else 0
    if info == (): return 0 if "#" in record else 1

    # Check if we have cached current values and use those
    key = (record, info)
    if key in cache:
        return cache[key]

    result = 0
    if record[0] in ".?": result += record_score(record[1:], info)
    if record[0] in "#?":
        if info[0] <= len(record) and "." not in record[:info[0]] and (info[0] == len(record) or record[info[0]] != "#"):
            result += record_score(record[info[0] + 1:], info[1:])

    # Store calculation result in cache for later lookups
    cache[key] = result
    return result


def main(filename):
    """
    # Results:
    """
    with open(filename) as f:
        lines = f.readlines()

    records = [line.split() for line in lines]

    possible1 = 0
    for record, info in records:
        possible1 += record_score(record, tuple(map(int, info.split(","))))
    print(f"Part1: {possible1}")

    possible2 = 0
    for record, info in records:
        possible2 += record_score("?".join([record] * 5), tuple(map(int, info.split(","))) * 5)
    print(f"Part2: {possible2}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
