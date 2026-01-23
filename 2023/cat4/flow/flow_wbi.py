import datetime
import logging
import os
import sys
from typing import List, Dict, Union, Set


def get_neighbouring_pixels(rows, row_idx, col_idx):
    """returns 2 to 4 neighbouring values"""
    neighbours = []
    num_rows = len(rows)
    num_cols = len(rows[0])
    potential_neighbour_indices = [
        (row_idx - 1, col_idx),
        (row_idx + 1, col_idx),
        (row_idx, col_idx - 1),
        (row_idx, col_idx + 1),
    ]
    for option in potential_neighbour_indices:
        if option[0] >= 0 and option[0] < num_rows and option[1] >= 0 and option[1] < num_cols:
            neighbours.append(rows[option[0]][option[1]])

    if len(neighbours) < 2 or len(neighbours) > 4:
        raise ValueError("Impossible")

    return neighbours


def find_endpoints(rows: List[List]) -> List[List]:
    """Returns an array of arrays, containing 0 or endpoints' value"""
    num_rows = len(rows)
    num_cols = len(rows[0])
    endpoint_rows = []
    for i in range(num_rows):
        endpoint_row = []
        for j in range(num_cols):
            value = rows[i][j]
            neighbour_values = get_neighbouring_pixels(rows, i, j)
            # If value appears only once in neighbour_values, then it's an endpoint
            num_occurrences = 0
            for neigh_val in neighbour_values:
                if value == neigh_val:
                    num_occurrences += 1
            if num_occurrences == 1:
                endpoint_row.append(value)
            else:
                endpoint_row.append(0)
        endpoint_rows.append(endpoint_row)
    return endpoint_rows


def map_neighbouring_regions(
    rows: List[List], endpoints: List[List], max_value: int
) -> Dict[int, Set]:
    num_rows = len(rows)
    num_cols = len(rows[0])

    # Initialize links to empty sets
    links: Dict[int, Set] = {value: set() for value in range(1, max_value + 1)}

    for i in range(num_rows - 1):
        for j in range(num_cols - 1):
            value = rows[i][j]
            endpoint = endpoints[i][j]

            right_value = rows[i + 1][j]
            right_endpoint = endpoints[i + 1][j]
            if not (endpoint and right_endpoint):
                # Add (bidirectional)
                links[value].add(right_value)
                links[right_value].add(value)

            bottom_value = rows[i][j + 1]
            bottom_endpoint = endpoints[i][j + 1]
            if not (endpoint and bottom_endpoint):
                links[value].add(bottom_value)
                links[bottom_value].add(value)

    return links


def solve_task(rows, num_rows, num_cols):
    max_value = 0
    for i in range(num_rows):
        max_row_value = max(rows[i])
        if max_row_value > max_value:
            max_value = max_row_value

    # Identify which pixels are 'endpoints'
    endpoints = find_endpoints(rows)

    # dictionary of sets with neighbouring regions for each region
    links = map_neighbouring_regions(rows, endpoints, max_value)

    # NOTE : could also represent links as an adjacency matrix?
    # Last step : Find largest set of disjoint (individual) regions
    # Start with trivial cases : combinations of one
    disjoint_combinations = set()
    for i in range(1, max_value + 1):
        disjoint_combinations.add((i,))

    vhdls = 0
    while disjoint_combinations:
        # In each iteration, attempt to find disjoint combinations that are one larger
        vhdls += 1
        logger.info(f"vhdls: {vhdls}. Number of options : {len(disjoint_combinations)} ")
        larger_disjoint_combinations: set = set()
        for disjoint_combination in disjoint_combinations:
            list_disjoint_combination = list(disjoint_combination)
            # Check if we can grow the current combination
            potential_growers = set([i for i in range(1, max_value + 1)])
            # Exclude regions that are already in
            potential_growers -= set(disjoint_combination)
            # Exclude neighbouring regions
            for element in disjoint_combination:
                potential_growers -= links[element]

            # It's good enough to select 1 grower in each iteration!
            # As long  it results in a new option
            for grower in potential_growers:
                # Create new set with old and new
                larger_disjoint_combination = tuple(list_disjoint_combination + [grower])
                if larger_disjoint_combination not in larger_disjoint_combinations:
                    larger_disjoint_combinations.add(larger_disjoint_combination)
                    break

        disjoint_combinations = larger_disjoint_combinations

    return vhdls


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

    line_idx = 1
    for entry in range(num_entries):
        logger.info(f"Reading entry {entry+1} out of {num_entries}")

        # Start of parsing
        num_rows, num_cols = map(int, input_lines[line_idx].strip().split())
        line_idx += 1

        rows = []
        for i in range(num_rows):
            row_values = list(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1
            rows.append(row_values)

        # Start of processing
        value = solve_task(rows, num_rows, num_cols)
        solution_str = f"{entry + 1} {value}"

        # Write to stdout
        print(solution_str)
        # Write to output file
        if output_filename:
            with open(output_filename, "a") as f:
                f.write(solution_str + "\n")

    logger.info(f"Done. Time elapsed: {datetime.datetime.now() - starttime}")
