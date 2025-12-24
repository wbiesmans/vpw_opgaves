"""
Homeswapping - Vlaamse Programmeerwedstrijd
Find maximum number of house swaps possible given preferences.
"""


def find_max_swaps(preferences):
    """
    Find maximum number of swaps in a permutation given preferences.

    Args:
        preferences: dict mapping house -> list of compatible houses

    Returns:
        Maximum number of houses that can be swapped
    """
    houses = list(preferences.keys())
    n = len(houses)
    max_swaps = 0

    # Try all possible permutations using backtracking
    def backtrack(assignment, used, swaps):
        nonlocal max_swaps

        if len(assignment) == n:
            max_swaps = max(max_swaps, swaps)
            return

        current_house = houses[len(assignment)]

        # Try assigning each compatible house
        for target in preferences[current_house]:
            if target not in used:
                used.add(target)
                new_swaps = swaps + (1 if target != current_house else 0)
                assignment.append(target)

                backtrack(assignment, used, new_swaps)

                assignment.pop()
                used.remove(target)

    backtrack([], set(), 0)
    return max_swaps


def solve_test_case(lines):
    """
    Parse and solve a single test case.

    Args:
        lines: list of strings, first is n, rest are preference lines

    Returns:
        Maximum number of swaps
    """
    n = int(lines[0])
    preferences = {}

    for i in range(1, n + 1):
        parts = lines[i].split()
        house = parts[0]
        compatible = set(parts)  # Includes the house itself and preferences
        preferences[house] = compatible

    return find_max_swaps(preferences)


def main():
    """Main function to read input and solve all test cases."""
    # Read from opgave.invoer file
    with open("temp/opgaves/2022/cat4/homeswap/wedstrijd.invoer", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    num_tests = int(lines[0])
    line_idx = 1

    for test_num in range(1, num_tests + 1):
        # Read number of houses for this test case
        n = int(lines[line_idx])
        test_lines = lines[line_idx : line_idx + n + 1]
        line_idx += n + 1

        result = solve_test_case(test_lines)
        print(f"{test_num} {result}")


if __name__ == "__main__":
    main()
