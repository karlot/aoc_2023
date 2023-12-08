part1 = "input.txt"
part2 = "input.txt"

# ------ part 1 ------
with open(part1, "r", encoding="utf8") as f:
    # Bag content of cubes
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    # Store valid games
    valid_games_sum = 0

    for game_line in f.readlines():
        [g, cube_sets] = game_line.split(":")
        
        # Game ID
        game = int(g.strip().split()[1])
        game_valid = True

        # Separate cube sets in each game (each set cannot have more cubes than total of each color)
        cube_set = [x.strip() for x in cube_sets.strip().split(";")]
        for cubes in cube_set:
            # Check each set if all combinations of set are passing possibility check
            c = [x.strip() for x in cubes.split(",")]
            for cube_def in c:
                [num, color] = cube_def.split()
                if (bag[color] < int(num)):
                    game_valid = False
        
        if game_valid:
            valid_games_sum += game
        
    print(f"Part1: {valid_games_sum}")


# ------ part 2 ------
with open(part2, "r", encoding="utf8") as f:

    game_powers = []
    for game_line in f.readlines():
        # Each game will store amount of colored cubes required to play it
        bag = {}

        # get Game ID, and sets
        [g, cube_sets] = game_line.split(":")
        game = int(g.strip().split()[1])

        # Separate cube sets in each game (each set cannot have more cubes than total of each color)
        cube_set = [x.strip() for x in cube_sets.strip().split(";")]
        for cubes in cube_set:
            # Check each set if all combinations of set are passing possibility check
            c = [x.strip() for x in cubes.split(",")]
            for cube_def in c:
                [num, color] = cube_def.split()
                if (not color in bag):
                    bag[color] = 0
                if (bag[color] < int(num)):
                    bag[color] = int(num)
        
        power = 1   # must start with 1 due to multiplication
        for x in bag.values():
            power *= x

        game_powers.append(power)
        
    print(f"Part2: {sum(game_powers)}")

