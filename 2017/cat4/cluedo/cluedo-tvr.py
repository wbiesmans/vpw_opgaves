import sys
import logging
import datetime
import dataclasses

@dataclasses.dataclass
class Question:
    player: str
    options: str
    answering_player: str

@dataclasses.dataclass
class Player:
    player: str
    possible_cards: list = dataclasses.field(default_factory=list)
    impossible_cards: set = dataclasses.field(default_factory=set)
    confirmed_cards: set = dataclasses.field(default_factory=set)

def process(questions):
    players = [Player("1"), Player("2"), Player("3"), Player("4")]

    for question in questions:
        logger.debug(f'Processing {question}')
        current_player = question.player
        options = question.options
        answering_player = question.answering_player

        if answering_player == "X":
            for player in players:
                if player.player == current_player:
                    continue
                player.impossible_cards = player.impossible_cards.union(options)
                logger.debug(f'Extended list of impossible cards for {player.player} to {player.impossible_cards}')
            continue

        next_player_index = int(current_player)
        next_player = players[next_player_index % len(players)]
        while(next_player.player not in [current_player, answering_player]):
            next_player.impossible_cards = next_player.impossible_cards.union(options)
            next_player_index += 1
            next_player = players[next_player_index % len(players)]
        if next_player.player == answering_player:
            next_player.possible_cards = next_player.possible_cards + [options]

    change = True
    while(change):
        change = False
        for player in players:
            for possible_cards in player.possible_cards:
                possible_cards = [possible_card for possible_card in possible_cards if possible_card not in player.impossible_cards]
                if len(possible_cards) == 1 and possible_cards[0] not in player.confirmed_cards:
                    change = True
                    player.confirmed_cards.add(possible_cards[0])
                    for player2 in players:
                        if player == player2:
                            continue
                        player2.impossible_cards.add(possible_cards[0])
    
    return ' '.join(''.join(sorted((player.confirmed_cards))) for player in players)


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
        number_of_persons, number_of_locations, number_of_weapons = tuple(map(int, input_lines[line_index].strip().split()))
        number_of_questions = int(input_lines[line_index+1].strip())
        questions = []
        for j in range(number_of_questions):
            player, options, answering_player = tuple(input_lines[line_index + 2 + j].strip().split())
            questions.append(Question(player, list(options), answering_player))
        logger.debug(f'{number_of_persons=}, {number_of_locations=}, {number_of_weapons}, {number_of_questions=}, {questions=}')
        line_index += number_of_questions + 2
        # End of parsing
        # Start of processing
        output_line = process(questions)
        # End of processing
        
        print(f'{i+1} {output_line}')
    
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')