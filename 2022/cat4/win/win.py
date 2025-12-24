# Recursive

from dataclasses import dataclass, field
from typing import List


@dataclass
class Outcome:
    winner: str
    numbers: List[int] = field(default_factory=list)

    def __repr__(self):
        numbers = sorted(list(set(self.numbers)))
        if self.winner == "a":
            return "win " + " ".join(map(str, numbers))
        elif self.winner == "b":
            return "verlies " + " ".join(map(str, numbers))
        else:
            assert not numbers
            return "gelijk"


def evaluate_sub_branch(
    winning_numbers, current_number, options_a, options_b, alice_move: bool, move_history
) -> Outcome:
    if alice_move:
        options = options_a
        current_player = "a"
        other_player = "b"
    else:
        options = options_b
        current_player = "b"
        other_player = "a"

    outcomes = []
    for move in options:
        new_number = current_number + move
        move_history += f"{current_player}{move}->{new_number} "
        if new_number > max(winning_numbers):
            return Outcome(winner="g")
        if new_number in winning_numbers:
            outcome = Outcome(winner=current_player, numbers=[new_number])
        else:
            outcome = evaluate_sub_branch(
                winning_numbers, new_number, options_a, options_b, not alice_move, move_history
            )
        outcomes.append(outcome)
    if outcomes[0].winner == current_player or outcomes[1].winner == current_player:
        winning_numbers = []
        if outcomes[0].winner == current_player:
            winning_numbers.extend(outcomes[0].numbers)
        if outcomes[1].winner == current_player:
            winning_numbers.extend(outcomes[1].numbers)
        print(move_history + f" ({current_player})")
        return Outcome(winner=current_player, numbers=winning_numbers)
    elif outcomes[0].winner == "g" or outcomes[1].winner == "g":
        print(move_history + " (g)")
        return Outcome(winner="g")
    elif outcomes[0].winner == other_player or outcomes[1].winner == other_player:
        winning_numbers = []
        if outcomes[0].winner == other_player:
            winning_numbers.extend(outcomes[0].numbers)
        if outcomes[1].winner == other_player:
            winning_numbers.extend(outcomes[1].numbers)
        print(move_history + f" ({other_player})")
        return Outcome(winner=other_player, numbers=winning_numbers)
    else:
        raise ValueError("Should not get here")


if __name__ == "__main__":
    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/win/voorbeeld.invoer") as f:
        lines = f.readlines()

    output_lines = []

    num_opgaves = int(lines[0])
    opgaves = []
    line_idx = 1
    lines_out = []
    for i in range(num_opgaves):
        aantal_winstgetallen = lines[line_idx].strip().split()
        line_idx = line_idx + 1
        winstgetallen = lines[line_idx].strip().split()
        winstgetallen = [int(x) for x in winstgetallen]
        line_idx += 1
        parts = lines[line_idx].strip().split()
        start_getal = int(parts[0])
        options_a = [int(parts[1]), int(parts[2])]
        options_b = [int(parts[3]), int(parts[4])]
        alice_move = True
        resultaat = evaluate_sub_branch(winstgetallen, start_getal, options_a, options_b, alice_move, f"{start_getal} ")
        print(resultaat)
        lines_out.append(f"{i+1} {resultaat}\n")
        line_idx += 1

    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/win/voorbeeld2.uitvoer", "w") as f:
        f.writelines(lines_out)
