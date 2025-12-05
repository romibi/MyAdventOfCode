from math import floor

DO_LOG = True
PUZZLE_NR = 2

def main():
    # puzzle_input = read_input('day_01_puzzle_input_small.txt')
    # puzzle_input = read_input('day_01_puzzle_input_small_custom.txt')
    puzzle_input = read_input('day_01_puzzle_input.txt')

    dial = 50
    password = parse_input(puzzle_input, dial)

    print()
    print(f"The password is {password}")

def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input, dial):
    password = 0
    for line in puzzle_input:
        dial, password = handle(line, dial, password)
    return password


def handle(line, dial, password):
    int_str = line[1:]
    rot = int(int_str)

    # dial_old = dial  # only used for PUZZLE_NR == 2
    add_to_rot = 0   # only used for PUZZLE_NR == 2

    if line[0] == 'L':
        add_to_rot = (100-dial) % 100  # only used for PUZZLE_NR == 2t
        dial -= rot
    elif line[0] == 'R':
        add_to_rot = dial # only used for PUZZLE_NR == 2t
        dial += rot
    else:
        print('!!!!!!!!!!!!!!!!! INVALID INPUT !!!!!!!!!!!!!!!!')

    additional_log = ""
    if PUZZLE_NR == 2:
        passed_zero_times = floor((rot+add_to_rot)/100)
        password += passed_zero_times
        #log(f"dial: {dial_old} → {dial}, rot: {rot}, add_to_rot: {add_to_rot}, extended_rot: {rot+add_to_rot}, passed 0: {(rot+add_to_rot)/100} times?")
        if passed_zero_times > 0:
            additional_log = f"; during this rotation it points at zero {passed_zero_times} time(s)"

    dial = dial % 100

    log(f"The dial is rotated {line.rstrip()} to point at {dial}{additional_log}.")

    if (PUZZLE_NR == 1) and (dial == 0):
        password += 1

    return dial, password

def log(text):
    if DO_LOG:
        print(text)

if __name__ == '__main__':
    main()