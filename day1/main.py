part1 = "input.txt"
part2 = "input.txt"

# ------ part 1 ------
with open(part1, "r", encoding="utf8") as f:
    calibration_value = 0
    for line in f.readlines():
        digits = []
        for char in line:
            if char.isdigit():
                digits.append(char)
        score = int(digits[0] + digits[-1])
        calibration_value += score

    print(f"Part1: {calibration_value}")


# ------ part 2 ------
with open(part2, "r", encoding="utf8") as f:
    calibration_value = 0
    for line in f.readlines():
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(c)
            for d, val in enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]):
                if line[i:].startswith(val):
                    digits.append(str(d + 1))
        score = int(digits[0] + digits[-1])
        calibration_value += score

    print(f"Part2: {calibration_value}")
