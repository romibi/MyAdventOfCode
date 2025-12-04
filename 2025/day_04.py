from numpy.matlib import empty

PUZZLE_NR=2

class Paper:
    def __init__(self):
        self.accessible = False

def main():
    # input = read_input('day_04_puzzle_1_input_small.txt')
    input = read_input('day_04_puzzle_1_input.txt')

    floor_map = generate_map(input)
    if PUZZLE_NR==1:
        floor_map, accessibility_count = calculate_floor_accessibility(floor_map)
    else:
        accessibility_count = 0

        while(True):
            floor_map, it_accessibility_count = calculate_floor_accessibility(floor_map)
            accessibility_count += it_accessibility_count
            print(f"Remove {it_accessibility_count} rolls of papaer:")
            print_map(floor_map)
            print("")
            floor_map = clean_map(floor_map)
            if it_accessibility_count == 0:
                break

    print_map(floor_map)
    print("")
    if PUZZLE_NR==1:
        print(f"There are {accessibility_count} Rolls accessible ...")
    else:
        print(f"There are {accessibility_count} Rolls removed ...")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def generate_map(input):
    width = len(input[0].strip())
    height = len(input)

    # floor_map = empty((height, width))
    floor_map = [[0 for x in range(width)] for y in range(height)]

    for y, line in enumerate(input):
        for x, char in enumerate(line.strip()):
            if char == "@":
                floor_map[y][x] = Paper()

    return floor_map #, width, height


def calculate_floor_accessibility(floor_map):
    width = len(floor_map[0])
    height = len(floor_map)
    accessibility_count = 0

    for y in range(0,height):
        for x in range(0,width):
            if floor_map[y][x]:
                accesible = calculate_paper_accessibility(y, x, floor_map)
                if accesible:
                    accessibility_count+=1
    return floor_map, accessibility_count


def calculate_paper_accessibility(y, x, floor_map):
    width = len(floor_map[0])
    height = len(floor_map)

    # row above:
    neighbor_count = 0
    if y > 0:
        if (x > 0) and floor_map[y-1][x-1]:
            neighbor_count += 1
        if floor_map[y-1][x]:
            neighbor_count += 1
        if (x < width-1) and floor_map[y-1][x+1]:
            neighbor_count += 1

    # same row
    if (x > 0) and floor_map[y][x-1]:
        neighbor_count += 1
    if (x < width-1) and floor_map[y][x+1]:
        neighbor_count += 1

    # row below
    if y < height-1:
        if (x > 0) and floor_map[y+1][x-1]:
            neighbor_count += 1
        if floor_map[y+1][x]:
            neighbor_count += 1
        if (x < width-1) and floor_map[y+1][x+1]:
            neighbor_count += 1

    if neighbor_count < 4:
        floor_map[y][x].accessible = True

    return floor_map[y][x].accessible


def clean_map(floor_map):
    width = len(floor_map[0])
    height = len(floor_map)

    for y in range(0,height):
        for x in range(0,width):
            if floor_map[y][x] and floor_map[y][x].accessible:
                floor_map[y][x] = None
    return floor_map


# added for part 2
def print_map(floor_map):
    width = len(floor_map[0])
    height = len(floor_map)

    for y in range(0,height):
        for x in range(0,width):
            if floor_map[y][x]:
                if floor_map[y][x].accessible:
                    print("X",end="")
                else:
                    print("@",end="")
            else:
                print(".",end="")
        print("")

if __name__ == '__main__':
    main()