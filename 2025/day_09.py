from typing import Tuple, List
from numpy import Infinity

PUZZLE_NR=2
USE_SMALL=False

# todo: do cleaner
global_red_tiles_clockwise = -1 # -1 unknown, 0 no, 1 yes

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
                    print(f"Valid Rectangle {self.pos}-{other_red_tile.pos}")
                    break
                else:
                    print(f"Invalid Rectangle {self.pos}-{other_red_tile.pos}")
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

    border_tiles = []
    first_corner_tile = None
    second_corner_tile = None

    for red_tile in red_tiles:
        if red_tile == tile_a or red_tile == tile_b:
            if not first_corner_tile:
                if red_tile == tile_a:
                    first_corner_tile = tile_a
                    second_corner_tile = tile_b
                else:
                    first_corner_tile = tile_b
                    second_corner_tile = tile_a
            last_red_tile = red_tile
            border_tiles.append(red_tile)
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

        if (
            ( ((red_tile.pos[0] == tile_a.pos[0]) or (red_tile.pos[0] == tile_b.pos[0]) ) and ( min(tile_a.pos[1],tile_b.pos[1]) <= red_tile.pos[1] <= max(tile_a.pos[1],tile_b.pos[1]))) or # same x as tile_a or tile_b and on y between tile_a and tile_b
            ( ((red_tile.pos[1] == tile_b.pos[1]) or (red_tile.pos[1] == tile_b.pos[1]) ) and ( min(tile_a.pos[0],tile_b.pos[0]) <= red_tile.pos[0] <= max(tile_a.pos[0],tile_b.pos[0])))
        ):
            border_tiles.append(red_tile)

        last_red_tile = red_tile

    # shit ... still possible that this rectangle is invalid. if it is in a concave part of the shape
    # now we need to know if the big shape is defined clockwise or counterclockwise
    # if we collect all tiles on the border of the rectangle and go around the rectangle the same direction
    # (clockwise/counterclockwise) the border tiles should be in the same order as in the shape list
    # otherwise we are on a concave part of the shape
    # LOOOOTS OF UGLY CODE FOLLOWS

    def IsClockwise(tiles):
        prev_tile = None
        prev_direction = -1 # -1: unknown, 0: up, 1: right, 2: down, 3: left
        turn_direction = 0 # positive value: clockwise, negative value: counterclockwise

        for tile in tiles:

            if not prev_tile:
                prev_tile = tile
                continue

            if prev_tile.pos[1] > tile.pos[1]:
                direction = 0 # up
            elif prev_tile.pos[0] < tile.pos[0]:
                direction = 1 # right
            elif prev_tile.pos[1] < tile.pos[1]:
                direction = 2 # down
            elif prev_tile.pos[0] > tile.pos[0]:
                direction = 3 # left
            else:
                assert False  # Shouldn't happen??

            if prev_direction == -1:
                prev_direction = direction
                prev_tile = tile
                continue

            if prev_direction == 0:
                if direction == 1:
                    turn_direction += 1 # up -> right: clockwise
                elif direction == 3:
                    turn_direction -= 1 # up -> left: counter clockwise
                else:
                    assert False  # Shouldn't happen??
            elif prev_direction == 1:
                if direction == 0:
                    turn_direction -= 1 # right -> up: counter clockwise
                elif direction == 2:
                    turn_direction += 1 # right -> down: clockwise
                else:
                    assert False  # Shouldn't happen??
            elif prev_direction == 2:
                if direction == 1:
                    turn_direction -= 1 # down -> right: counter clockwise
                elif direction == 3:
                    turn_direction += 1 # down -> left: clockwise
                else:
                    assert False  # Shouldn't happen??
            elif prev_direction == 3:
                if direction == 0:
                    turn_direction += 1 # left -> up: clockwise
                elif direction == 2:
                    turn_direction -= 1 # left -> down: counter clockwise
                else:
                    assert False  # Shouldn't happen??
            else:
                assert False # Shouldn't happen??

            prev_tile = tile
            prev_direction = direction

        return turn_direction > 0

    # shit ... still possible that this rectangle is invalid. if it is in a concave part of the shape
    # now we need to know if the big shape is defined clockwise or counterclockwise
    # if we collect all tiles on the border of the rectangle and go around the rectangle the same direction
    # (clockwise/counterclockwise) the border tiles should be in the same order as in the shape list
    # otherwise we are on a concave part of the shape

    # print("Analyze if the red tile list is clockwise ... ")
    # todo: nicer
    global global_red_tiles_clockwise
    if global_red_tiles_clockwise == -1:
        shape_list_is_clockwise = IsClockwise(red_tiles)
        if shape_list_is_clockwise:
            global_red_tiles_clockwise = 1
        else:
            global_red_tiles_clockwise = 0
    else:
        shape_list_is_clockwise = global_red_tiles_clockwise==1
    # print(f"The red tile list is clockwise? {shape_list_is_clockwise}")

    ## if clockwise
    ## 1-----
    ## |  A  |
    ##  -----2
    ## -> each next border tile after 1 should have same y and higher x as 1 (or last border tile), or same x as 2 but lower y than 2 (but higher y than last border tile), or be 2
    ## -> each next border tile after 2 should have same y and lower x as 2 (or last border tile), or same x as 1 but higher y than 1 (but lower y than last border tile)

    ## 2-----
    ## |  B  |
    ##  -----1
    ## -> each next border tile after 1 should have same y and lower x as 1 (or last border tile), or same x as 2 but higher y than 2 (but lower y than last border tile), or be 2
    ## -> each next border tile after 2 should have same y and hgiher x as 2 (or last border tile), or same x as 1 but lower y than 1 (but higher y than last border tile)

    ##  -----1
    ## |  C  |
    ## 2-----
    ## -> each next border tile after 1 should have same x and higher y as 1 (or last border tile), or same y as 2 but higher x than 2 (but lower x than last border tile), or be 2
    ## -> each next border tile after 2 should have same x and lower y as 2 (or last border tile), or same y as 1 but lower x than 1 (but higher x than last border tile)

    ##  -----2
    ## |  D  |
    ## 1-----
    ## -> each next border tile after 1 should have same x and lower y as 1 (or last border tile), or same y as 2 but lower x than 2 (but higher x than last border tile), or be 2
    ## -> each next border tile after 2 should have same x and higher y as 2 (or last border tile), or same y as 2 but higher x than 1 (but lower x than last border tile)

    case = ""

    if (first_corner_tile.pos[0] < second_corner_tile.pos[0]) and (first_corner_tile.pos[1] < second_corner_tile.pos[1]):
        case = "A"
    elif (first_corner_tile.pos[0] > second_corner_tile.pos[0]) and (first_corner_tile.pos[1] > second_corner_tile.pos[1]):
        case = "B"
    elif (first_corner_tile.pos[0] > second_corner_tile.pos[0]) and (first_corner_tile.pos[1] < second_corner_tile.pos[1]):
        case = "C"
    elif (first_corner_tile.pos[0] < second_corner_tile.pos[0]) and (first_corner_tile.pos[1] > second_corner_tile.pos[1]):
        case = "D"
    else:
        # The corners are on the same x or same y axis. lets assume they are small and irrelevant:
        return False


    def valid_right_of(start_tile, end_tile, last_tile, tile): # can be used for A Step 1 and B Step 3
        if tile.pos[1] != start_tile.pos[1]:
            return False

        return last_tile.pos[0] < tile.pos[0] <= end_tile.pos[0]

    def valid_right_down_of(_, end_tile, last_tile, tile): # can be used for A Step 2 and B Step 4
        if tile.pos[0] != end_tile.pos[0]:
            return False

        return last_tile.pos[1] <= tile.pos[1] < end_tile.pos[1]

    def valid_left_of(start_tile, end_tile, last_tile, tile): # can be used for A Step 3 and B Step 1
        if tile.pos[1] != start_tile.pos[1]:
            return False

        return end_tile.pos[0] <= tile.pos[0] < last_tile.pos[0]

    def valid_left_above_of(_, end_tile, last_tile, tile): # can be used for A Step 4 and B Step 2
        if tile.pos[0] != end_tile.pos[0]:
            return False

        return end_tile.pos[1] < tile.pos[1] <= last_tile.pos[1]

    def valid_below_of(start_tile, end_tile, last_tile, tile): # can be used for C Step 1 and D Step 3
        if tile.pos[0] != start_tile.pos[0]:
            return False

        return last_tile.pos[1] < tile.pos[1] <= end_tile.pos[1]

    def valid_below_left_of(_, end_tile, last_tile, tile): # can be used for C Step 2 and D Step 4
        if tile.pos[1] != end_tile.pos[1]:
            return False

        return end_tile.pos[0] < tile.pos[0] <= last_tile.pos[0]

    def valid_above_of(start_tile, end_tile, last_tile, tile): # cen be used for C Step 3 and D Step 1
        if tile.pos[0] != start_tile.pos[0]:
            return False

        return end_tile.pos[1] <= tile.pos[1] < last_tile.pos[1]

    def valid_above_right_of(_, end_tile, last_tile, tile): # can be used for C Step 4 and D Step 2
        if tile.pos[1] != end_tile.pos[1]:
            return False

        return last_tile.pos[0] <= tile.pos[0] < end_tile.pos[0]

    if case == "A":
        first_border_condition = valid_right_of
        second_border_condition = valid_right_down_of
        third_border_condition = valid_left_of
        forth_border_condition = valid_left_above_of
    elif case == "B":
        first_border_condition = valid_left_of
        second_border_condition = valid_left_above_of
        third_border_condition = valid_right_of
        forth_border_condition = valid_right_down_of
    elif case == "C":
        first_border_condition = valid_below_of
        second_border_condition = valid_below_left_of
        third_border_condition = valid_above_of
        forth_border_condition = valid_above_right_of
    elif case == "D":
        first_border_condition = valid_above_of
        second_border_condition = valid_above_right_of
        third_border_condition = valid_below_of
        forth_border_condition = valid_below_left_of
    else:
        assert False # shouldn't happen


    found_2 = False
    took_corner = False
    last_border_tile = None

    # print(f"Check {len(border_tiles)} Border tiles ...")

    while border_tiles[0] != first_corner_tile:
        border_tiles = border_tiles[1:] + border_tiles[:1]

    if not shape_list_is_clockwise:
        # the booleans above can only be used for clockwise validity check (i think).
        # lets reverse the order but because we still want to start with first_corner_tile, rotate first once more
        border_tiles = border_tiles[1:] + border_tiles[:1]
        border_tiles.reverse()

    for border_tile in border_tiles:
        if border_tile == first_corner_tile:
            last_border_tile = border_tile
            took_corner = False
            continue

        if border_tile == second_corner_tile:
            found_2 = True
            took_corner = False
            last_border_tile = border_tile
            continue

        if not found_2 and not took_corner:
            if not first_border_condition(first_corner_tile, second_corner_tile, last_border_tile, border_tile):
                if second_border_condition(first_corner_tile, second_corner_tile, last_border_tile, border_tile):
                    took_corner = True
                else:
                    return False
        elif not found_2 and took_corner:
            if not second_border_condition(first_corner_tile, second_corner_tile, last_border_tile, border_tile):
                return False
        elif found_2 and not took_corner:
            if not third_border_condition(second_corner_tile, first_corner_tile, last_border_tile, border_tile):
                if forth_border_condition(second_corner_tile, first_corner_tile, last_border_tile, border_tile):
                    took_corner = True
                else:
                    return False
        elif found_2 and took_corner:
            if not forth_border_condition(second_corner_tile, first_corner_tile, last_border_tile, border_tile):
                return False
        else:
            assert False # should not happen
        last_border_tile = border_tile
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