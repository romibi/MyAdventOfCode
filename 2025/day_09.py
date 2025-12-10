from typing import Tuple, List

PUZZLE_NR=1
USE_SMALL=False


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

    def get_biggest_rectangle(self, red_tiles: List['RedTile']):
        item = next(iter(self.rectangle_sizes_with_other_tiles.items()))
        obj_id = item[0]
        size = item[1]
        other_red_tile = next((obj for obj in red_tiles if id(obj) == obj_id), None)
        return other_red_tile, size



def main():
    if USE_SMALL:
        puzzle_input = read_input('day_09_puzzle_input_small.txt')
    else:
        puzzle_input = read_input('day_09_puzzle_input.txt')

    red_tiles = parse_input(puzzle_input)
    calculate_all_distances(red_tiles)

    tile_a, tile_b, size = find_biggest_rect(red_tiles)

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


def find_biggest_rect(red_tiles):
    biggest_rectangle_tile_a = red_tiles[0]
    biggest_rectangle_tile_b, biggest_size = red_tiles[0].get_biggest_rectangle(red_tiles)

    for red_tile in red_tiles:
        other_red_tile, local_biggest_size = red_tile.get_biggest_rectangle(red_tiles)
        if local_biggest_size>biggest_size:
            biggest_size = local_biggest_size
            biggest_rectangle_tile_a = red_tile
            biggest_rectangle_tile_b = other_red_tile

    return biggest_rectangle_tile_a, biggest_rectangle_tile_b, biggest_size


if __name__ == '__main__':
    main()