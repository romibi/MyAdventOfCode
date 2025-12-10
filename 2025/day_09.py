from typing import Tuple, List
from numpy import Infinity

PUZZLE_NR=2
USE_SMALL=True


class RedTile:
    def __init__(self, pos: Tuple[int, int]):
        self.pos = pos
        self.rectangle_sizes_with_other_tiles = {}


    def rectangle_size_to(self, other: 'RedTile'):
        return (abs(self.pos[0]-other.pos[0])+1)*(abs(self.pos[1]-other.pos[1])+1)


    def calculate_rectangle_sizes_to(self, red_tiles: List['RedTile']):
        for red_tile in red_tiles:
            if red_tile  == self:
                continue
            size = self.rectangle_size_to(red_tile )
            self.rectangle_sizes_with_other_tiles[id(red_tile)] = size

        self.rectangle_sizes_with_other_tiles = dict(sorted(self.rectangle_sizes_with_other_tiles.items(), key=lambda item: item[1], reverse=True))

    def get_biggest_rectangle(self, red_tiles: List['RedTile'], validate=False):
        size = Infinity
        other_red_tile = None
        # New for Puzzle 2: do not only get first but validate if ok and iterate further if not
        for item in self.rectangle_sizes_with_other_tiles.items():
            obj_id = item[0]
            size = item[1]
            other_red_tile = next((obj for obj in red_tiles if id(obj) == obj_id), None)
            if validate:
                if validate_rectangle(self, other_red_tile, red_tiles):
                    break
            else:
                break
        return other_red_tile, size

# New for Puzzle 2
def validate_rectangle(tile_a, tile_b, red_tiles):

    # If there are Red Tiles inside, it's a guaranteed issue
    prohibited_area_min_x = min(tile_a.pos[0], tile_b.pos[0]) + 1
    prohibited_area_min_y = min(tile_a.pos[1], tile_b.pos[1]) + 1

    prohibited_area_max_x = max(tile_a.pos[0], tile_b.pos[0]) - 1
    prohibited_area_max_y = max(tile_a.pos[1], tile_b.pos[1]) - 1

    last_red_tile = red_tiles[-1]

    for red_tile in red_tiles:
        if red_tile == tile_a or red_tile == tile_b:
            last_red_tile = red_tile
            continue

        if ((prohibited_area_min_x <= red_tile.pos[0] <= prohibited_area_max_x) and
                (prohibited_area_min_y <= red_tile.pos[1] <= prohibited_area_max_y)):
            return False

        # We can't say "ok" yet. if the line from last to this goes through our rectangle its bad as well
        if not ((last_red_tile.pos[0] < prohibited_area_min_x and red_tile.pos[0] < prohibited_area_min_x) or # both on left side
            (last_red_tile.pos[0] > prohibited_area_max_x and red_tile.pos[0] > prohibited_area_max_x) or # both on right side
            (last_red_tile.pos[1] < prohibited_area_min_y and red_tile.pos[1] < prohibited_area_min_y) or # both above
            (last_red_tile.pos[1] > prohibited_area_max_y and red_tile.pos[1] > prohibited_area_max_y)):  # both below
            return False

        last_red_tile = red_tile

    # TODO: shit ... still possible that this rectangle is invalid. if it is in a concave part of the shape
    # now we need to know if the big shape is defined clockwise or counterclockwise
    # if we collect all tiles on the border of the rectangle and go around the rectangle the same direction
    # (clockwise/counterclockwise) the border tiles should be in the same order as in the shape list
    # otherwise we are on a concave part of the shape

    return True


def main():
    if USE_SMALL:
        puzzle_input = read_input('day_09_puzzle_input_small.txt')
    else:
        puzzle_input = read_input('day_09_puzzle_input.txt')

    red_tiles = parse_input(puzzle_input)
    calculate_all_distances(red_tiles)

    if PUZZLE_NR == 1:
        tile_a, tile_b, size = find_biggest_rect(red_tiles)
    else:
        if USE_SMALL:
            generate_area_map(red_tiles)
        tile_a, tile_b, size = find_biggest_rect(red_tiles, True)


    print("")
    print(f"The biggest rectangle is from {tile_a.pos} to {tile_b.pos} and is {size} big.")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input) -> List[RedTile]:
    red_tiles: List[RedTile] = []
    for line in puzzle_input:
        coordinates = line.strip().split(',')
        red_tile = RedTile((int(coordinates[0]), int(coordinates[1])))
        red_tiles.append(red_tile)

    return red_tiles


def calculate_all_distances(red_tiles):
    for red_tile in red_tiles:
        red_tile.calculate_rectangle_sizes_to(red_tiles)


def find_biggest_rect(red_tiles, validate=False):
    biggest_rectangle_tile_a = red_tiles[0]
    biggest_rectangle_tile_b, biggest_size = red_tiles[0].get_biggest_rectangle(red_tiles, validate)

    for red_tile in red_tiles:
        other_red_tile, local_biggest_size = red_tile.get_biggest_rectangle(red_tiles, validate)
        if local_biggest_size>biggest_size:
            biggest_size = local_biggest_size
            biggest_rectangle_tile_a = red_tile
            biggest_rectangle_tile_b = other_red_tile

    return biggest_rectangle_tile_a, biggest_rectangle_tile_b, biggest_size


# =============================
# Code below only used for visualization of small version of Puzzle 2 (not for the result anymore, too slow)
# =============================

def set_char_in_line(orig_line, column_nr, new_char):
    return orig_line[:column_nr] + new_char + orig_line[column_nr+1:]


def generate_area_map(red_tiles):
    x = 0
    y = 0
    for red_tile in red_tiles:
        x = max(red_tile.pos[0],x)
        y = max(red_tile.pos[1],y)

    empty_line = "."*(x+2) # +1 for 0 coordinate, +1 for empty row on positive side
    area_map = [empty_line for _ in range(0,y+1)] # +1 as range is exclusive, +1 for empty line at end

    # for line in area_map:
    #     print(line)
    #
    # print("")

    last_red_tile = None

    for red_tile in red_tiles:
        x = red_tile.pos[0]
        y = red_tile.pos[1]

        if last_red_tile:
            fill_tiles_inbetween(area_map, last_red_tile, red_tile, "X")

        area_map[y] = set_char_in_line(area_map[y],x,"#")
        last_red_tile = red_tile

    fill_tiles_inbetween(area_map, last_red_tile, red_tiles[0], "X")

    # for line in area_map:
    #     print(line)
    # print("")

    fill_tiles_inside(area_map, red_tiles[0], last_red_tile)

    for line in area_map:
        print(line)

    return area_map


def fill_tiles_inbetween(area_map, tile_a, tile_b, new_char):
    if tile_a.pos[0] == tile_b.pos[0]:
        # Horizontal movement
        x = tile_a.pos[0]
        small_y = min(tile_a.pos[1], tile_b.pos[1])
        big_y = max(tile_a.pos[1], tile_b.pos[1])

        for y in range(small_y+1, big_y):
            area_map[y] = set_char_in_line(area_map[y], x, new_char)

    elif tile_a.pos[1] == tile_b.pos[1]:
        # Vertical movement
        small_x = min(tile_a.pos[0], tile_b.pos[0])
        big_x = max(tile_a.pos[0], tile_b.pos[0])
        y = tile_a.pos[1]

        for x in range(small_x+1, big_x):
            area_map[y] = set_char_in_line(area_map[y], x, new_char)


def fill_tiles_inside(area_map, first_tile, last_tile):
    # noinspection PyShadowingNames
    def find_any_coordinates_inside(area_map, first_tile, last_tile):
        # Not completely sure if there's an easier way, but when closing the loop from the last to the first tile,
        # one tile before getting back to the first one, one side is inside, the other outside.
        # Let's pick the positive direction first and check each coordinate if there is another red or green tile first
        # or the area_map border. If it's not the area_map border we crossed the inside. Otherwise, go back to before checking each
        # tile in positive direction and go once to the negative direction

        x_start = first_tile.pos[0]
        y_start = first_tile.pos[1]

        max_x = len(area_map[0])
        max_y = len(area_map)

        search_horizontal = True

        if first_tile.pos[0]>last_tile.pos[0]:
            # go left once, then search down
            x_start -= 1
            search_horizontal = False
        elif first_tile.pos[0]<last_tile.pos[0]:
            # go right once, then search down
            x_start += 1
            search_horizontal = False
        elif first_tile.pos[1]>last_tile.pos[1]:
            # go up once, then search right
            y_start -= 1
            search_horizontal = True
        elif first_tile.pos[1]<last_tile.pos[1]:
            # go down once, then search right
            y_start += 1
            search_horizontal = True

        x = x_start
        y = y_start

        if search_horizontal:
            x += 1
            while x < max_x:
                if area_map[y][x] != ".":
                    return x-1, y
                x += 1

            return x_start-1, y_start

        else:
            y += 1
            while y < max_y:
                if area_map[y][x] != ".":
                    return x, y-1
                y += 1

            return x_start, y_start-1

    # noinspection PyShadowingNames
    def fill_neighbors(area_map, x, y):
        fill_char = "x"
        # up
        if area_map[y - 1][x] == ".":
            area_map[y - 1] = set_char_in_line(area_map[y - 1], x, fill_char)
            fill_neighbors(area_map, x, y - 1)
        # right
        if area_map[y][x + 1] == ".":
            area_map[y] = set_char_in_line(area_map[y], x + 1, fill_char)
            fill_neighbors(area_map, x + 1, y)
        # down
        if area_map[y + 1][x] == ".":
            area_map[y + 1] = set_char_in_line(area_map[y + 1], x, fill_char)
            fill_neighbors(area_map, x, y + 1)
        # left
        if area_map[y][x - 1] == ".":
            area_map[y] = set_char_in_line(area_map[y], x - 1, fill_char)
            fill_neighbors(area_map, x - 1, y)

    fill_start_x, fill_start_y = find_any_coordinates_inside(area_map, first_tile, last_tile)
    fill_neighbors(area_map, fill_start_x, fill_start_y)


if __name__ == '__main__':
    main()