from math import sqrt
from typing import Tuple, Optional, List

from numpy import Infinity

PUZZLE_NR=1
next_circuit_id = 0

class Circuit:
    def __init__(self, circuit_id:int):
        self.circuit_id = circuit_id
        self.junction_boxes: List[JunctionBox] = []

    def add(self, junction_box: 'JunctionBox'):
        assert junction_box.circuit is None
        junction_box.circuit = self
        self.junction_boxes.append(junction_box)


    def move_all(self, circuit: 'Circuit'):
        for junction_box in circuit.junction_boxes:
            junction_box.circuit = None
            self.add(junction_box)
        circuit.junction_boxes.clear()


class JunctionBox:
    def __init__(self, pos: Tuple[int, int, int], circuit: Optional[Circuit] = None):
        self.pos = pos
        self.circuit = circuit

        self.directly_connected_to: List[Circuit] = []
        self.skipped_direct_connection: List[Circuit] = []

        self.unconnected_distances = {}


    def distance_to(self, other: 'JunctionBox'):
        return sqrt(((self.pos[0]-other.pos[0])**2) + ((self.pos[1]-other.pos[1])**2) + ((self.pos[2]-other.pos[2])**2))


    def calculate_distances_to(self, junction_boxes: List['JunctionBox']):
        for junction_box in junction_boxes:
            if junction_box == self:
                continue
            dist = self.distance_to(junction_box)
            self.unconnected_distances[id(junction_box)] = dist

        self.unconnected_distances = dict(sorted(self.unconnected_distances.items(), key=lambda item: item[1]))


    def connect_to(self, other: 'JunctionBox') -> Tuple[Circuit, bool]:
        assert (self.circuit is None and other.circuit is None) or (self.circuit != other.circuit)
        new_circuit = False
        if self.circuit:
            if other.circuit:
                self.circuit.move_all(other.circuit)
            else:
                self.circuit.add(other)
        else:
            if other.circuit:
                other.circuit.add(self)
            else:
                global next_circuit_id
                new_circuit = Circuit(next_circuit_id)
                next_circuit_id += 1
                new_circuit.add(self)
                new_circuit.add(other)
                new_circuit = True

        self.directly_connected_to.append(other)
        other.directly_connected_to.append(self)
        del self.unconnected_distances[id(other)]
        del other.unconnected_distances[id(self)]

        assert isinstance(self.circuit, Circuit)
        print(f"Connected ({self.pos}) to ({other.pos}) in {new_circuit} Circuit {self.circuit.circuit_id}")

        return self.circuit, new_circuit


def main():

    USE_SMALL = False

    if USE_SMALL:
        puzzle_input = read_input('day_08_puzzle_input_small.txt')
        connection_count = 10
    else:
        puzzle_input = read_input('day_08_puzzle_input.txt')
        connection_count = 1000

    junction_boxes = parse_input(puzzle_input)
    calculate_all_distances(junction_boxes)

    circuits = make_connections(junction_boxes, connection_count)
    puzzle_result = calculate_size_of_x_largest(circuits, 3)

    print("")
    print(f"The sizes of the largest circuits combined is: {puzzle_result}")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input) -> List[JunctionBox]:
    junctions_boxes: List[JunctionBox] = []
    for line in puzzle_input:
        coordinates = line.strip().split(',')
        junctions_box = JunctionBox((int(coordinates[0]), int(coordinates[1]), int(coordinates[2])))
        junctions_boxes.append(junctions_box)

    return junctions_boxes


def calculate_all_distances(junction_boxes):
    for junction_box in junction_boxes:
        junction_box.calculate_distances_to(junction_boxes)


def find_shortest_open_connection(junction_boxes) -> Tuple[JunctionBox, JunctionBox]:
    assert len(junction_boxes)>=2

    current_shortest_dist = Infinity
    current_shortest: Tuple[JunctionBox, JunctionBox] = (junction_boxes[0], junction_boxes[1])

    for junction_box_a in junction_boxes:
        item = next(iter(junction_box_a.unconnected_distances.items()))
        obj_id = item[0]
        dist = item[1]
        junction_box_b = next((obj for obj in junction_boxes if id(obj) == obj_id), None)

        if dist<current_shortest_dist:
            current_shortest = (junction_box_a, junction_box_b)
            current_shortest_dist = dist

    # # First attempt, but enables only one new connection per second -> about 16 minutes
    # for a in range(0, len(junction_boxes)-1):
    #     junction_box_a = junction_boxes[a]
    #     for b in range(a+1, len(junction_boxes)):
    #         junction_box_b = junction_boxes[b]
    #         if junction_box_b in junction_box_a.directly_connected_to or junction_box_b in junction_box_a.skipped_direct_connection:
    #             continue
    #         dist = junction_box_a.distance_to(junction_box_b)
    #         if dist<current_shortest_dist:
    #             current_shortest = (junction_box_a, junction_box_b)
    #             current_shortest_dist = dist

    return current_shortest


def make_connections(junction_boxes, connection_count):
    circuits: List[Circuit] = []
    for i in range(0, connection_count):
        junction_box1, junction_box2 = find_shortest_open_connection(junction_boxes)
        if junction_box1.circuit is not None and junction_box2.circuit is not None and junction_box1.circuit==junction_box2.circuit:
            junction_box1.skipped_direct_connection.append(junction_box2)
            junction_box2.skipped_direct_connection.append(junction_box1)
            del junction_box1.unconnected_distances[id(junction_box2)]
            del junction_box2.unconnected_distances[id(junction_box1)]
            print(f"Skipped connection between {junction_box1.pos} and {junction_box2.pos}")
        elif junction_box1.circuit is None or junction_box2.circuit is None or junction_box1.circuit != junction_box2.circuit:
            connected_circuit, new_circuit = junction_box1.connect_to(junction_box2)
            if new_circuit:
                circuits.append(connected_circuit)
    return circuits



def calculate_size_of_x_largest(circuits, x):
    result_value = 1

    sorted_circuits = sorted(circuits, key=lambda c: len(c.junction_boxes), reverse=True)

    i = 0
    for circuit in sorted_circuits:
        if i==x:
            break
        result_value *= len(circuit.junction_boxes)
        i += 1

    assert i==x

    return result_value


if __name__ == '__main__':
    main()