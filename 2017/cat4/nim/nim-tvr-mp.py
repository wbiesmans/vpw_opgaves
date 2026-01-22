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

from functools import lru_cache

@lru_cache(None)
def is_winning_misere(piles):
    # Base Case: If no stones are left, you "win" because 
    # the opponent was forced to take the last stone.
    if sum(piles) == 0:
        return True

    # Standard Minimax: Can I make a move that leaves my opponent in a losing state?
    for i, count in enumerate(piles):
        for take in range(1, count + 1):
            next_state = list(piles)
            next_state[i] -= take
            
            # Sort to keep the memoization table small
            next_state_tuple = tuple(sorted(next_state))
            
            # If the move leads to a state where the opponent LOSES, you WIN
            if not is_winning_misere(next_state_tuple):
                return True
                
    return False


def find_all_misere_winning_moves(initial_piles):
    winning_moves = []
    for i, count in enumerate(initial_piles):
        for take in range(1, count + 1):
            next_state = list(initial_piles)
            next_state[i] -= take
            
            if not is_winning_misere(tuple(sorted(next_state))):
                winning_moves.append(next_state)  
    return winning_moves
        
def print_lock(lock, string: str) -> None:
    lock.acquire()
    try:
        print(string)
    finally:
        lock.release()
    return

def process(semaphore: multiprocessing.synchronize.Semaphore, index: int, lock: multiprocessing.synchronize.Lock, rows: list[int]) -> None:
    try:
        moves = find_all_misere_winning_moves(rows)
        if not moves:
            print_lock(lock=lock, string=f"{index} HOPELOOS")
            return
        for result in sorted(moves):
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