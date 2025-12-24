def get_score(oplossing):
    alfabet = "abcdefghijklmnopqrstuvwxyz"
    score = 0
    for idx, character in enumerate(oplossing):
        if character != alfabet[idx]:
            score += 1

    return score


def find_num_replacements(opgave):
    current_solutions = [""]
    for from_house in opgave:
        next_solutions = []
        for to_house in from_house:
            for solution in current_solutions:
                if to_house not in solution:
                    next_solutions.append((solution + to_house))
        # print(next_solutions)
        current_solutions = next_solutions

    max_score = 0
    best_solution = ""
    for solution in current_solutions:
        score = get_score(solution)
        if score > max_score:
            best_solution = solution
            max_score = score

    return max_score, best_solution


if __name__ == "__main__":
    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/homeswap/voorbeeld.invoer") as f:
        lines = f.readlines()

    output_lines = []

    num_opgaves = int(lines[0])
    opgaves = []
    line_idx = 1
    for i in range(num_opgaves):
        num_houses = int(lines[line_idx])
        line_idx += 1
        opgave = []
        for j in range(num_houses):
            opgave.append(lines[line_idx + j].strip().split(" "))
        line_idx += num_houses

        result, best_solution = find_num_replacements(opgave)

        print(f"{i+1} {result}")

        output_lines.append(f"{i+1} {result}\n")

        opgaves.append(opgave)

    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/homeswap/voorbeeld2.uitvoer", "w") as f:
        f.writelines(output_lines)
