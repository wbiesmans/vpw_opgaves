def simuleer_tonnen(west, oost, hoogte_west, hoogte_oost):
    if oost > west:
        oost_to_west = True
        high = oost
        low = west
    else:
        oost_to_west = False
        high = west
        low = oost

    while high > low:
        if high > max(hoogte_west, hoogte_oost):
            high = high - 1
            low = low + 1
        else:
            break

    if high == low:
        return "gelijk"
    elif oost_to_west:
        return f"{low} {high}"
    else:
        return f"{high} {low}"


if __name__ == "__main__":
    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/waterput4/wedstrijd.invoer") as f:
        lines = f.readlines()

    output_lines = []

    num_opgaves = int(lines[0])
    opgaves = []
    line_idx = 1
    lines_out = []
    for i in range(num_opgaves):
        parts = lines[line_idx].strip().split()
        parts = [int(part) for part in parts]
        parts = tuple(parts)

        resultaat = simuleer_tonnen(*parts)
        print(resultaat)
        lines_out.append(f"{i+1} {resultaat}\n")
        line_idx += 1

    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/waterput4/wedstrijd2.uitvoer", "w") as f:
        f.writelines(lines_out)
