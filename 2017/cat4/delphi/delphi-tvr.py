import sys
import logging
import datetime
import dataclasses
import math


def process(no_questions, age, questions_asked=0):
    if no_questions >= age:
        return questions_asked + 1
    if no_questions == 1:
        return age + questions_asked
    if no_questions > 1:
        i = 1
        total = 0
        while(total < age):
            total += i
            i += 1
        i = i - 1
        logger.debug(f'Calling recursive function with {no_questions=}, age={i}')
        return process(no_questions - 1, i - 1, questions_asked + 1)


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
    for i in range(number_of_entries):
        logger.info(f'Reading entry {i+1} out of {number_of_entries}')
        
        # Start of parsing
        no_questions, age = tuple(map(int, input_lines[line_index + i].strip().split()))
        logger.debug(f'{no_questions=}, {age=}')
        # End of parsing
        # Start of processing
        output_lines = process(no_questions, age)
        # End of processing
        print(f'{i+1} {output_lines}')
    
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')