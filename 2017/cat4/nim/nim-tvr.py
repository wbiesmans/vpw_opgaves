import sys
import logging
import datetime
import dataclasses
import multiprocessing
import multiprocessing.synchronize
import typing
import copy
import collections

sys.setrecursionlimit(1500)

def game_round(rows, player_one=True, memo=None):
    if memo is None:
        memo = collections.defaultdict()
    player_win_result = True
    if not player_one:
        player_win_result = False
    if not any(rows):
        return player_win_result, None
    state = (tuple(sorted(rows)), player_one)
    if state in memo.keys():
        return memo[state]
    results = []
    for index, stones in enumerate(rows):
        if stones == 0:
            continue
        for stones_to_take in range(1, stones + 1):
            rows_copy = rows[:index] + [stones - stones_to_take] + rows[index+1:]
            result_bool, _ = game_round(rows_copy, not player_one, memo)
            if result_bool == player_win_result:
                memo[state] = (player_win_result, None)
                results.append(rows_copy)
    if results:
        return player_win_result, results
    memo[state] = (not player_win_result, None)
    return not player_win_result, None
        
def print_lock(lock, string: str) -> None:
    lock.acquire()
    try:
        print(string)
    finally:
        lock.release()
    return

def process(semaphore: multiprocessing.synchronize.Semaphore, index: int, lock: multiprocessing.synchronize.Lock, rows: list[int]) -> None:
    try:
        _, results = game_round(rows=rows, memo=None)
        if results is None:
            print_lock(lock=lock, string=f"{index} HOPELOOS")
            return
        for result in sorted(results):
            print_lock(lock=lock, string=f'{index} {' '.join(map(str, result))}')
    except RecursionError:
        logger.warning(f'Recursion error for {index}')
        return
    

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
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
    lock = multiprocessing.Lock()
    semamphore = multiprocessing.Semaphore(8)
    processes = []
    for i in range(number_of_entries):
        logger.info(f'Reading entry {i+1} out of {number_of_entries}')
        
        # Start of parsing
        row = tuple(map(int, input_lines[line_index].strip().split()))
        number_of_rows = row[0]
        rows = list(row[1:])
        logger.info(f'{number_of_rows=}, {rows=}')
        line_index += 1
        # End of parsing

        # Start of processing
        p = multiprocessing.Process(target=process, args=(semamphore, i + 1, lock, rows))
        p.start()
        processes.append(p)
        # End of processing
    i = 1
    for p in processes:
        logger.info(f'Waiting for process {i} to complete')
        p.join()
        i += 1
            
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')