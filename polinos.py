import dataclasses
from typing import List


@dataclasses.dataclass
class Coordinate:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    # Sort coordinates for consistent ordering
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


@dataclasses.dataclass
class Polino:
    coordinates: List[Coordinate]

    # To determine uniqueness of polinos
    def __hash__(self):
        return hash(tuple(sorted(self.coordinates)))

    # To sort polinos for consistent ordering
    def __lt__(self, other):
        return sorted(self.coordinates) < sorted(other.coordinates)

    def __gt__(self, other):
        return sorted(self.coordinates) > sorted(other.coordinates)

    def __eq__(self, other):
        return set(self.coordinates) == set(other.coordinates)


def draw_polinos(polinos: List[Polino]) -> None:
    import matplotlib.pyplot as plt

    for idx, polino in enumerate(polinos):
        xs = [coord.x for coord in polino.coordinates]
        ys = [coord.y for coord in polino.coordinates]

        plt.figure()
        plt.scatter(xs, ys)
        for x, y in zip(xs, ys):
            plt.text(x, y, f"({x},{y})")
        plt.title(f"Polino {idx + 1} with {len(polino.coordinates)} cells")
        plt.xlim(-1, max(xs) + 2)
        plt.ylim(-1, max(ys) + 2)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.grid(True)
        plt.show()


def rotate(polino: Polino):
    rotated_coords = [Coordinate(-coord.y, coord.x) for coord in polino.coordinates]
    # Normalize to first quadrant
    min_x = min(coord.x for coord in rotated_coords)
    min_y = min(coord.y for coord in rotated_coords)
    normalized_coords = [Coordinate(coord.x - min_x, coord.y - min_y) for coord in rotated_coords]
    return Polino(coordinates=normalized_coords)


def all_rotations(polino: Polino) -> List[Polino]:
    rotations = [polino]
    current = polino
    for _ in range(3):
        current = rotate(current)
        rotations.append(current)
    return rotations


def prune_rotations(polinos: List[Polino]) -> List[Polino]:
    unique_polinos = []
    seen_representations = set()

    for polino in polinos:
        rotations = all_rotations(polino)

        # Keep the minimal representation as the canonical one
        min_representation = min(rotations)

        if min_representation not in seen_representations:
            seen_representations.add(min_representation)
            unique_polinos.append(polino)

    return unique_polinos


def get_polinos(n: int, remove_rotations=False) -> List[Polino]:
    if n == 1:
        return [Polino(coordinates=[Coordinate(0, 0)])]
    else:
        start_polinos = get_polinos(n - 1)
        new_polinos = []
        for polino in start_polinos:
            grown_polinos = grow(polino)

            new_polinos.extend(grown_polinos)

        # Remove exact (coordinate-wise) duplicates
        unique_polinos = set(new_polinos)

        # Prune those that are just rotations of each other.
        # Only do this in last step, otherwise growth will be incomplete.
        if remove_rotations:
            unique_polinos = prune_rotations(list(unique_polinos))

        new_polinos = sorted(list(unique_polinos))

        return new_polinos


def grow(polino: Polino) -> List[Polino]:
    # Only add coordinates in first quadrant
    potential_new_coords = set()
    for coord in polino.coordinates:
        potential_new_coords.add(Coordinate(coord.x + 1, coord.y))
        potential_new_coords.add(Coordinate(coord.x - 1, coord.y))
        potential_new_coords.add(Coordinate(coord.x, coord.y + 1))
        potential_new_coords.add(Coordinate(coord.x, coord.y - 1))

    # Remove coordinates already taken
    taken_coordinates = set(polino.coordinates)
    potential_new_coords = potential_new_coords - taken_coordinates

    # Create new polinos
    for new_coord in potential_new_coords:
        new_polino_coords = polino.coordinates.copy() + [new_coord]
        # Shift coordinates to first quadrant
        min_x = min(coord.x for coord in new_polino_coords)
        min_y = min(coord.y for coord in new_polino_coords)
        normalized_coords = [Coordinate(coord.x - min_x, coord.y - min_y) for coord in new_polino_coords]
        yield Polino(coordinates=normalized_coords)


if __name__ == "__main__":

    for n in range(1, 11):
        print(f"Generating polinos with {n} cells")
        polinos = get_polinos(n, remove_rotations=True)
        print(f"Found: {len(polinos)} unique polinos with {n} cells")
        # for p in polinos:
        #     print(p.coordinates)
        # draw_polinos(polinos)

# Mistakes made:
# - Thought initially checking for rotations would not be necessary if we omitted straight line duplicates,
#    e.g. by fixing the first two coordinates to be (0,0) and (1,0). However, e.g. for n=4, the L shape was duplicated
# - You should allow polyomino's with negative coordinates when growing, normalize to first quadrant after
#    Otherwise, you will not catch e.g. 'cross' polyomino shapes (think of a plus sign).

# Thought of most of the strategy (representation as list of coordinates, limit to first quadrant,
# iterative growth + prune strategy) myself on paper, but adjusted details through trial-and-error
# Had autocomplete help from copilot for rotating/normalizing the polinos and for how to support sorting/hasing
