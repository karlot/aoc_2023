import sys
import math

def main(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    # [ Part 1 ]
    # --------------------------------
    times = []
    distances = []
    for line in lines:
        if "Time:" in line:
            times = [int(l) for l in line.split()[1:]]
        else:
            distances = [int(l) for l in line.split()[1:]]

    races = zip(times, distances)
    race_wins = []
    for duration, record in races:
        wins = 0
        for t in range(1, duration):
            if (duration - t) * t > record:
                wins += 1
        race_wins.append(wins)
    print(f"Part1: {math.prod(race_wins)}")

    # [ Part 2 ]
    # --------------------------------
    time = 0
    distance = 0
    for line in lines:
        if "Time:" in line:
            time = int("".join(line.split()[1:]))
        else:
            distance = int("".join(line.split()[1:]))

    wins = 0
    for t in range(1, time):
        if (time - t) * t > distance:
            wins += 1
    print(f"Part2: {wins}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need input file!")
        exit(1)
    main(sys.argv[1])
