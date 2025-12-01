DO_LOG = True
PUZZLE_NR = 2

def main():
    #input = read_input('day_01_puzzle_1_input_small.txt')
    input = read_input('day_01_puzzle_1_input.txt')

    dial = 50
    password = parse_input(input, dial)

    print()
    print(f"The password is {password}")

def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(input, dial):
    password = 0
    for line in input:
        dial, password = handle(line, dial, password)
    return password


def handle(line, dial, password):
    int_str = line[1:]
    rot = int(int_str)

    if line[0] == 'L':
        dial -= rot
    elif line[0] == 'R':
        dial += rot
    else:
        print('!!!!!!!!!!!!!!!!! INVALID INPUT !!!!!!!!!!!!!!!!')

    if (PUZZLE_NR == 2) and (dial > 99 or dial < 0):
        password += 1

    dial = dial % 100

    log(f"The dial is rotated {line.rstrip()} to point at {dial}.")

    if dial == 0:
        password += 1

    return dial, password

def log(text):
    if DO_LOG:
        print(text)

if __name__ == '__main__':
    main()