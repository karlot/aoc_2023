# from collections import defaultdict
# from rich.pretty import pprint

# input_file = "example.txt"
input_file = "input.txt"

seeds = []
maps = {}

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    with open(input_file, "r", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]

    current_map = ""
    for line in lines:
        if line == "": continue         # ignore empty
        if line.startswith("seeds:"):   # read seeds to be planted
            seeds = [int(seed) for seed in line.split()[1:]]
            continue
        
        if "map:" in line:
            current_map = line.split()[0]
            maps[current_map] = []
            continue

        # other lines are entries of the map
        [dst_range_start, src_range_start, range_len] = line.split()
        maps[current_map].append([int(src_range_start), int(dst_range_start), int(range_len)])

    # Sort maps by source id (lookup value)
    for m in maps:
        maps[m].sort()
    
    # pprint(maps)
    def get_next_relation(id, map):
        for [s, d, r] in maps[map]:
            if s <= id < s + r:
                # id is withing rage, return 
                return d + id - s
        return id

        
    def seed_to_location(seed):
        soil = get_next_relation(seed, 'seed-to-soil')
        fertilizer = get_next_relation(soil,'soil-to-fertilizer')
        water = get_next_relation(fertilizer, 'fertilizer-to-water')
        light = get_next_relation(water, 'water-to-light')
        temperature = get_next_relation(light,'light-to-temperature')
        humidity = get_next_relation(temperature,'temperature-to-humidity')
        location = get_next_relation(humidity,'humidity-to-location')
        # pprint([seed, soil, fertilizer, water, light, temperature, humidity, location])
        return location

    part1_seed_locations = [seed_to_location(s) for s in seeds]
    print(f"Part1: {min(part1_seed_locations)}")
    
    chunk = 1
    part2_smallest = None
    for [start_seed, num_seeds] in chunks(seeds, 2):
        print(f"Processing {chunk} seeds chunk out of {int(len(seeds) / 2)}, with {num_seeds} seeds")
        for i in range(num_seeds):
            loc = seed_to_location(start_seed + i)
            if part2_smallest == None or loc < part2_smallest:
                part2_smallest = loc
        chunk += 1
    print(f"Part2: {part2_smallest}")


#// Run the code...
if __name__ == "__main__":
    main()