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

    started_at_0 = dial==0  # only used for PUZZLE_NR == 2

    if line[0] == 'L':
        dial -= rot
    elif line[0] == 'R':
        dial += rot
    else:
        print('!!!!!!!!!!!!!!!!! INVALID INPUT !!!!!!!!!!!!!!!!')

    additional_log = ""
    if (PUZZLE_NR == 2) and ((not started_at_0) and (dial > 100 or dial < 0)):
        password += 1
        additional_log = f"; during this rotation it points at 0 once"

    dial = dial % 100

    log(f"The dial is rotated {line.rstrip()} to point at {dial}{additional_log}.")

    if dial == 0:
        password += 1

    return dial, password

def log(text):
    if DO_LOG:
        print(text)

if __name__ == '__main__':
    main()