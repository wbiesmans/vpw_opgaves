import bisect


def omphalos(array):
    sorted_array = sorted(array)
    output = []
    for idx, number in enumerate(array):
        number_smaller = bisect.bisect_left(sorted_array, number)
        # number_smaller = sorted_array.index(number)
        output.append(number_smaller)
        sorted_array.pop(number_smaller)
    return output


if __name__ == "__main__":
    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/untitled4/wedstrijd.invoer") as f:
        lines = f.readlines()

    output_lines = []

    num_opgaves = int(lines[0])
    opgaves = []
    line_idx = 1
    lines_out = []
    for i in range(num_opgaves):
        array_size = lines[line_idx].strip().split()
        line_idx = line_idx + 1
        array = lines[line_idx].strip().split()
        array = [int(x) for x in array]
        resultaat = omphalos(array)
        resultaat = [str(x) for x in resultaat]
        print(str(i))
        lines_out.append(f"{i+1} {' '.join(resultaat)}\n")
        line_idx += 1

    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/untitled4/wedstrijd2.uitvoer", "w") as f:
        f.writelines(lines_out)
