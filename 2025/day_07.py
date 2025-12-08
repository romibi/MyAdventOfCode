PUZZLE_NR=2

def main():
    # puzzle_input = read_input('day_07_puzzle_input_small.txt')
    puzzle_input = read_input('day_07_puzzle_input.txt')

    diagram = remove_newlines(puzzle_input)

    for line in diagram:
        print(line)

    print("")
    print("Processing:")

    diagram = remove_newlines(puzzle_input)
    split_count = update_diagram(diagram)

    print("")
    print(f"The Beam Split {split_count} times.")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def remove_newlines(lines):
    return [line.rstrip() for line in lines]


def is_extended_tachyon_beam(column_nr, prev_line, line):
    if line[column_nr] == '^':
        # Beam can't extend on a splitter
        return False
    if prev_line[column_nr] == "|" or prev_line[column_nr] == "S":
        # Alternatively if ... == "."
        # Beam extends if there's a tachyon beam above
        return True
    return False

def is_split_tachyon_beam(column_nr, prev_line, line):
    if line[column_nr] != '^':
        # Beam can only split on a splitter
        return False
    if prev_line[column_nr] == "|" or prev_line[column_nr] == "S":
        # Alternatively if ... == "."
        # Beam splits if there's a tachyon beam above
        return True
    return False


def update_diagram(diagram):
    split_count = 0
    print(diagram[0])

    # Next block only used for PUZZLE 2
    last_line_tachyon_count = [1 if s == "S" else 0 for s in diagram[0]]
    this_line_tachyon_count = [0 for _ in last_line_tachyon_count]

    for line_nr in range(1, len(diagram)):
        prev_line = diagram[line_nr-1]
        unmodified_line = diagram[line_nr]
        for column_nr in range(0, len(unmodified_line)):
            if is_extended_tachyon_beam(column_nr, prev_line, unmodified_line):
                diagram[line_nr] = set_tachyon_beam(diagram[line_nr], column_nr)
                this_line_tachyon_count[column_nr] += last_line_tachyon_count[column_nr] # only used for PUZZLE 2
            if is_split_tachyon_beam(column_nr, prev_line, unmodified_line):
                if column_nr>=1:
                    diagram[line_nr] = set_tachyon_beam(diagram[line_nr], column_nr-1)
                    this_line_tachyon_count[column_nr-1] += last_line_tachyon_count[column_nr] # only used for PUZZLE 2
                if column_nr<(len(unmodified_line)-1):
                    diagram[line_nr] = set_tachyon_beam(diagram[line_nr], column_nr+1)
                    this_line_tachyon_count[column_nr+1] += last_line_tachyon_count[column_nr] # only used for PUZZLE 2
                if PUZZLE_NR == 1:
                    split_count += 1
        print(diagram[line_nr])

        # Next block only used for PUZZLE 2
        # print(*this_line_tachyon_count, sep="")
        last_line_tachyon_count = this_line_tachyon_count
        this_line_tachyon_count = [0 for _ in last_line_tachyon_count]

    if PUZZLE_NR==2:
        return sum(last_line_tachyon_count)
    return split_count


def set_tachyon_beam(orig_line, column_nr):
    return orig_line[:column_nr] + "|" + orig_line[column_nr+1:]


if __name__ == '__main__':
    main()