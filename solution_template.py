import datetime
import logging
import os
import sys
import typing


def solve_task(inputs):
    pass


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
        num_objects = int(input_lines[line_idx].strip())
        line_idx += 1

        objects = []
        for i in range(num_objects):
            start_hour, start_min, end_hour, end_min = tuple(
                map(int, input_lines[line_idx].strip().split())
            )
            line_idx += 1
            start = 60 * start_hour + start_min
            end = 60 * end_hour + end_min
            objects.append(tuple([start, end]))

        # Start of processing
        value = solve_task(objects)
        solution_str = f"{entry + 1} {value}"

        # Write to stdout
        print(solution_str)
        # Write to output file
        if output_filename:
            with open(output_filename, "a") as f:
                f.write(solution_str + "\n")

    logger.info(f"Done. Time elapsed: {datetime.datetime.now() - starttime}")
