import datetime
import logging
import os
import sys
import typing


def solve_task(budgets, food_trucks):

    # Optimization : stop when budget - new_spent > min_future_spends
    # Stop when

    amounts_spent = [0]
    for prices in food_trucks:  # increasing
        new_amounts = []
        for price in prices:  # increasing
            for spent in amounts_spent:
                new_spent = spent + price
                new_amounts.append(new_spent)
        new_amounts = list(set(new_amounts))  # remove duplicates
        amounts_spent = sorted(new_amounts)

    solvable_budgets = []
    for budget in budgets:
        if budget in amounts_spent:
            solvable_budgets.append(budget)

    if solvable_budgets:
        return " ".join(map(str, solvable_budgets))
    else:
        return "GEEN"


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

        budgets = list(map(int, input_lines[line_idx].strip().split()))[1:]
        line_idx += 1
        num_food_trucks = int(input_lines[line_idx].strip())
        line_idx += 1
        all_prices = []
        for j in range(num_food_trucks):
            prices = list(map(int, input_lines[line_idx].strip().split()))[1:]
            line_idx += 1
            all_prices.append(prices)

        # Start of processing
        value = solve_task(budgets, all_prices)
        solution_str = f"{entry + 1} {value}"

        # Write to stdout
        print(solution_str)
        # Write to output file
        if output_filename:
            with open(output_filename, "a") as f:
                f.write(solution_str + "\n")

    logger.info(f"Done. Time elapsed: {datetime.datetime.now() - starttime}")
