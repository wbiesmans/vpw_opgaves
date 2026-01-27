import sys
import logging
import datetime
import dataclasses
import typing

@dataclasses.dataclass
class Item:
    value: int
    requirements: tuple[int]

def solve_1_knapsack_01(capacity: int, items: list[Item]):
    number_of_items = len(items)
    # initialize zeroes
    dp = [[0] * (capacity + 1) for _ in range(number_of_items + 1)]
    # loop over all items, and all capacities up till the actual capacity
    # ranges are +1 because we need to track 0 items and 0 capacity as an option
    for current_item_plus_one_index in range(1, number_of_items + 1):
        current_item = items[current_item_plus_one_index - 1]
        for current_capacity in range(capacity + 1):
            current_item_requirement = current_item.requirements[0]
            if current_item_requirement <= current_capacity:
                dp[current_item_plus_one_index][current_capacity] = max(dp[current_item_plus_one_index - 1][current_capacity], current_item.value + dp[current_item_plus_one_index - 1][current_capacity - current_item_requirement])
            else:
                dp[current_item_plus_one_index][current_capacity] = dp[current_item_plus_one_index - 1][current_capacity]
    value_to_return = dp[-1][-1]
    # backtrack to find actual items. Start with the maximum (last value in the matrix), move upwards (item -1), and if there's change, the item was used.
    items_to_return = ()
    current_capacity = capacity
    for current_item_plus_one_index in range(number_of_items, 0, -1):
        if dp[current_item_plus_one_index][current_capacity] == dp[current_item_plus_one_index-1][current_capacity]:
            continue
        item = items[current_item_plus_one_index - 1]
        items_to_return += (item,)
        current_capacity -= item.requirements[0]
    return value_to_return, items_to_return

def solve_2_knapsack_01(capacity: tuple[int], items: list[Item]):
    number_of_items = len(items)
    # initialize zeroes
    dp = [[[0] * (capacity[1] + 1) for _ in range (capacity[0] + 1)] for _ in range(number_of_items + 1)]
    # loop over all items, and all capacities up till the actual capacity
    # ranges are +1 because we need to track 0 items and 0 capacity as an option
    for current_item_plus_one_index in range(1, number_of_items + 1):
        current_item = items[current_item_plus_one_index - 1]
        for current_capacity_0 in range(capacity[0] + 1):
            for current_capacity_1 in range(capacity[1] + 1):
                current_item_requirement_0, current_item_requirement_1 = current_item.requirements
                skip = dp[current_item_plus_one_index - 1][current_capacity_0][current_capacity_1]
                if current_item_requirement_0 <= current_capacity_0 and current_item_requirement_1 <= current_capacity_1:
                    take = current_item.value + dp[current_item_plus_one_index - 1][current_capacity_0 - current_item_requirement_0][current_capacity_1 - current_item_requirement_1]
                    dp[current_item_plus_one_index][current_capacity_0][current_capacity_1] = max(skip, take)
                else:
                    dp[current_item_plus_one_index][current_capacity_0][current_capacity_1] = skip
    value_to_return = dp[-1][-1][-1]
    # backtrack to find actual items. Start with the maximum (last value in the matrix), move upwards (item -1), and if there's change, the item was used.
    items_to_return = ()
    current_capacity_0 = capacity[0]
    current_capacity_1 = capacity[1]
    for current_item_plus_one_index in range(number_of_items, 0, -1):
        if dp[current_item_plus_one_index][current_capacity_0][current_capacity_1] == dp[current_item_plus_one_index-1][current_capacity_0][current_capacity_1]:
            continue
        item = items[current_item_plus_one_index - 1]
        items_to_return += (item,)
        current_capacity_0 -= item.requirements[0]
        current_capacity_1 -= item.requirements[1]
    return value_to_return, items_to_return

def solve_n_knapsack_01(capacities: tuple[int], items: list[Item], item_index: int = 0, memo: typing.Union[None, dict[tuple[int, tuple[int]]]] = None) -> tuple[int, tuple[Item]]:
    if memo is None:
        memo = {}
    
    # End of list
    if item_index == len(items):
        return 0, tuple()
    
    # State in memo
    state = (item_index, capacities)
    if state in memo:
        return memo[state]
    
    # Option 1: skip current item:
    result_weight, result_items = solve_n_knapsack_01(tuple(capacities), items, item_index + 1, memo)

    # Option 2: take current item
    current_item = items[item_index]
    fits_in_knapsack = all(requirement <= current_capacity for current_capacity, requirement in zip(capacities, current_item.requirements))
    
    result_items_with = None
    if fits_in_knapsack:
        new_capacities = tuple(current_capacity - requirement for current_capacity, requirement in zip(capacities, current_item.requirements))
        result_weight_with, result_items_with = solve_n_knapsack_01(new_capacities, items, item_index + 1, memo)
        result_weight_with += current_item.value
        result_items_with = (current_item,) + result_items_with
    
    if result_items_with and result_weight_with > result_weight:
        result_items = result_items_with
        result_weight = result_weight_with
    
    memo[state] = result_weight, result_items
    return result_weight, result_items

def process(stock, orders):
    value, items = solve_2_knapsack_01(stock, orders)
    logger.info(f'{value=} {items=}')
    return value

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    
    if len(sys.argv) <= 1:
        logger.info('No arguments, reading from standard input')
        input_lines = sys.stdin.readlines()
    else:
        logger.info(f'Arguments provided, reading {sys.argv[1]}')
        with open(sys.argv[1], 'r') as input_file:
            input_lines = input_file.readlines()

    starttime = datetime.datetime.now()

    number_of_entries = int(input_lines[0].strip())
    logger.info(f'Number of entries: {number_of_entries}')

    line_index = 1
    for i in range(number_of_entries):
        logger.info(f'Reading entry {i+1} out of {number_of_entries}')
        
        # Start of parsing
        product_a, product_b, clients = tuple(map(int, input_lines[line_index].strip().split()))
        stock = (product_a, product_b)
        orders = []
        for j in range(clients):
            requirements = tuple(map(int, input_lines[line_index + 1 + j].strip().split()))
            order = Item(1, requirements)
            orders.append(order)
        line_index += clients + 1
        # End of parsing
        # Start of processing
        output_line = process(stock, orders)
        # End of processing
        
        print(f'{i+1} {output_line}')
    
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')