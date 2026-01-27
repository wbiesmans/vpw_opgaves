import datetime
import logging
import os
import sys
import typing
import itertools
import bisect

def lis(nums):
    if not nums:
        return 0
    
    tails = []
    for x in nums:
        # Find the index where x would fit in the sorted 'tails' list
        idx = bisect.bisect_left(tails, x)
        
        if idx == len(tails):
            # x is larger than any element in tails, extend the subsequence
            tails.append(x)
        else:
            # Replace the existing element at idx with x
            # This maintains the smallest possible tail for that length
            tails[idx] = x
            
    return len(tails)

def get_lis_subsequence(nums):
    if not nums:
        return []

    n = len(nums)
    tails_indices = []  # Stores indices of the smallest tail for each length
    predecessor = [-1] * n  # Tracks the index of the previous element in the LIS

    for i, x in enumerate(nums):
        # We need to compare values, so we use the values at the stored indices
        current_tails_values = [nums[idx] for idx in tails_indices]
        idx = bisect.bisect_left(current_tails_values, x)

        if idx > 0:
            # The element before this one in the subsequence is the current tail 
            # of the subsequence one length shorter
            predecessor[i] = tails_indices[idx - 1]

        if idx == len(tails_indices):
            tails_indices.append(i)
        else:
            tails_indices[idx] = i

    # Reconstruct the subsequence by backtracking through the predecessors
    lis = []
    curr = tails_indices[-1]
    while curr != -1:
        lis.append(nums[curr])
        curr = predecessor[curr]
    
    return lis[::-1] # Reverse to get the correct order

def get_card_list_int(cards, suit_order):
    card_values = []
    for card in cards:
        suit = card[0]
        face = card[1:]
        try:
            face_int = int(face)
        except ValueError:
            match face:
                case 'B':
                    face_int = 11
                case 'V':
                    face_int = 12
                case 'H':
                    face_int = 13
                case 'A':
                    face_int = 14
        suit_index = list(suit_order).index(suit)
        card_value = face_int + 14 * suit_index
        card_values.append(card_value)
    return card_values

def get_valid_orders(suits):
    colors = {
        'K': 'Black',
        'S': 'Black',
        'H': 'Red',
        'R': 'Red'
    }

    if len(suits) == 1:
        return [tuple(suits)]
    
    if len(suits) == 2:
        return list(itertools.permutations(suits))

    valid_permutations = []
    for permutation in itertools.permutations(suits):
        if all(colors[permutation[i]] != colors[permutation[i+1]] for i in range(len(suits) - 1)):
            valid_permutations.append(permutation)
    return valid_permutations

def get_suits(cards):
    suits = set()
    for card in cards:
        suits.add(card[0])
    return suits

def solve_task(number_of_cards, cards):
    suits = get_suits(cards)
    valid_orders = get_valid_orders(suits)
    min_changes = float('inf')
    for order in valid_orders:
        card_list_int = get_card_list_int(cards, order)
        changes = int(number_of_cards) - lis(card_list_int)
        if changes < min_changes:
            min_changes = changes
    return min_changes


def read_value(line, cast=None):
    value = input_lines[line_index].strip()
    if cast:
        value = cast(value)
    return value

def read_tuple(line, cast=None):
    values = input_lines[line_index].strip().split()
    if cast:
        values = tuple(map(cast, values))
    else:
        values = tuple(values)
    return values

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    if len(sys.argv) <= 1:
        # Read from standard input
        logger.info("No arguments, reading from standard input")
        input_lines = sys.stdin.readlines()
        output_filename = None
    else:
        # Read from file
        logger.info(f"Arguments provided, reading {sys.argv[1]}")
        with open(sys.argv[1], "r") as input_file:
            input_lines = input_file.readlines()
        output_filename = sys.argv[1].replace("invoer", "uitvoer.tvr")
        # Clear output file if it exists
        if os.path.exists(output_filename):
            os.remove(output_filename)

    starttime = datetime.datetime.now()

    num_entries = int(input_lines[0].strip())
    logger.info(f"Number of entries: {num_entries}")

    line_index = 1
    for entry in range(num_entries):
        logger.info(f"Reading entry {entry+1} out of {num_entries}")

        # Start of parsing
        input_line = read_tuple(input_lines[line_index])
        line_index += 1

        # Start of processing
        value = solve_task(input_line[0], input_line[1:])
        solution_str = f"{entry + 1} {value}"

        # Write to stdout
        print(solution_str)
        # Write to output file
        if output_filename:
            with open(output_filename, "a") as f:
                f.write(solution_str + "\n")

    logger.info(f"Done. Time elapsed: {datetime.datetime.now() - starttime}")
