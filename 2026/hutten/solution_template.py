import datetime
import logging
import os
import sys
import typing
from math import inf


import sys
import logging
import datetime
import dataclasses
import heapq
import multiprocessing
import collections
import typing


@dataclasses.dataclass
class Edge:
    node_a: str
    node_b: str
    weight: int
    bidirectional: bool = True
    mandatory: bool = False

    def start_nodes(self) -> list[str]:
        if self.bidirectional:
            return [self.node_a, self.node_b]
        return [self.node_a]

    def other_end(self, node: str) -> str:
        if node == self.node_a:
            return self.node_b
        return self.node_a

    def __hash__(self) -> int:
        return hash((self.node_a, self.node_b, self.weight, self.bidirectional, self.mandatory))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False
        return (
            self.node_a == other.node_a
            and self.node_b == other.node_b
            and self.weight == other.weight
            and self.bidirectional == other.bidirectional
            and self.mandatory == other.mandatory
        )

    def __repr__(self) -> str:
        return f"{self.node_a} -> {self.node_b} ({self.weight})"


@dataclasses.dataclass
class Path:
    edges: list[Edge]
    nodes: list[str]

    def distance(self) -> int:
        return sum([edge.weight for edge in self.edges])

    def min_est_distance(self) -> int:
        num_nodes = len(graph_matrix)
        missing_nodes = [node for node in range(num_nodes) if node not in self.nodes]
        total_dist = 0
        for node in missing_nodes:
            total_dist += graph_matrix[node][0]
        return self.distance() + total_dist + graph_matrix[self.nodes[0]][self.nodes[-1]]

    def __lt__(self, other) -> bool:
        return self.min_est_distance() < other.min_est_distance()

    def __repr__(self) -> str:
        return ", ".join(
            [
                f"{self.nodes[i-1]} -> {self.nodes[i]} ({self.edges[i-1].weight})"
                for i in range(1, len(self.nodes))
            ]
        )


class Graph:
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        self.edgemap = self.build_edge_map(edges)

    def __repr__(self) -> str:
        return ", ".join(map(str, [edge for edge in self.edges]))

    def get_nodes(self) -> set[str]:
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.node_a)
            nodes.add(edge.node_b)
        return nodes

    def neigbouring_nodes(self, node: str) -> set[str]:
        neighbours = set()
        for edge in self.edgemap[node]:
            neighbour = edge.other_end(node)
            neighbours.add(neighbour)
        return neighbours

    def build_edge_map(self, edges: list[Edge]) -> dict[str, list[Edge]]:
        edgemap = collections.defaultdict(list)
        for edge in edges:
            edgemap[edge.node_a].append(edge)
            if edge.bidirectional:
                edgemap[edge.node_b].append(edge)
        return edgemap

    def reachable_nodes_dfs(self, node: str, visited_nodes: set = None) -> set[str]:
        if visited_nodes is None:
            visited_nodes = set()
        visited_nodes.add(node)
        for edge in self.edgemap[node]:
            dest_node = edge.other_end(node)
            if dest_node in visited_nodes:
                continue
            self.reachable_nodes_dfs(node=dest_node, visited_nodes=visited_nodes)
        return visited_nodes

    def state_space_search(
        self, end: str, frontier: tuple[float, list[Path]] = None, nodes=None
    ) -> tuple[int, Path]:
        """
        Performs a state-space search using a priority queue to find the shortest
        path that satisfies all mandatory edge requirements.

        The algorithm explores the graph by treating the combination of (visited edges,
        current node) as a unique state. This allows it to solve complex routing
        problems where the same node might be visited multiple times to satisfy
        edge constraints.

        Args:
            frontier: A list used as a min-heap (via heapq) containing tuples of
                (estimated_total_distance, Path).
            end: The target node identifier to reach.

        Returns:
            A tuple of (min_distance, optimal_path):
                - min_distance (float): The total weight of the shortest path found
                that covers all mandatory edges. Defaults to infinity if none found.
                - optimal_path (Path or None): The Path object containing the sequence
                of edges and nodes. Returns None if no valid path reaches the end.

        Notes:
            - The algorithm utilizes a `state_memo` dictionary to prune paths that
            reach the same state (same edges traversed and same current node)
            with a higher cost.
            - Validity is strictly defined by the inclusion of all edges in the
            graph marked as `mandatory`.
        """
        if frontier is None:
            frontier = [(0, Path([], [0]))]
        min_distance = float("inf")
        optimal_path = None
        state_memo = dict()
        while frontier:
            _, most_promising_path = heapq.heappop(frontier)
            if most_promising_path.nodes[-1] in most_promising_path.nodes[:-2] and (
                len(most_promising_path.nodes) < len(nodes) + 1
            ):
                continue
            if most_promising_path.min_est_distance() >= min_distance:
                continue
            if len(most_promising_path.edges) > len(nodes):
                continue
            state = (frozenset(most_promising_path.edges), most_promising_path.nodes[-1])
            distance = most_promising_path.distance()
            if state in state_memo and state_memo[state] <= distance:
                continue
            state_memo[state] = distance
            if most_promising_path.nodes[-1] == end:
                if all([node in most_promising_path.nodes for node in nodes]):
                    if distance < min_distance:
                        min_distance = distance
                        optimal_path = most_promising_path
                    continue

            for edge in self.edgemap[most_promising_path.nodes[-1]]:
                next_path = Path(
                    most_promising_path.edges + [edge],
                    most_promising_path.nodes + [edge.other_end(most_promising_path.nodes[-1])],
                )
                heapq.heappush(frontier, (next_path.min_est_distance(), next_path))
        return min_distance, optimal_path

    def bellman_ford(
        self, start: str
    ) -> tuple[typing.Union[dict[str, float], float], typing.Union[dict[str, Edge], None]]:
        """
        Computes the shortest paths from a starting node to all other nodes using
        the Bellman-Ford algorithm.

        This implementation supports both directed and bidirectional edges and
        can detect negative weight cycles. If a negative cycle is reachable from
        the start node, the function indicates this by returning negative infinity.

        Args:
            start: The identifier (name or ID) of the source node to start from.

        Returns:
            A tuple containing:
                - distances: A dictionary mapping node IDs to their shortest distance
                from the start. If a negative cycle is detected, returns float('-inf').
                - used_edges: A dictionary mapping node IDs to the Edge object used
                to reach them (the predecessor). If a negative cycle is detected,
                returns None.

        Note:
            The complexity is O(V * E), where V is the number of vertices and E
            is the number of edges. This is slower than Dijkstra's but necessary
            for graphs with negative edge weights.
        """

        # Helper to get all directed versions of the edges
        def get_all_directed():
            for edge in self.edges:
                yield (edge, edge.node_a, edge.node_b, edge.weight)
                if edge.bidirectional:
                    yield (edge, edge.node_b, edge.node_a, edge.weight)

        nodes_count = len(self.get_nodes())
        distances = {node: float("inf") for node in self.get_nodes()}
        used_edges = {node: None for node in self.get_nodes()}
        distances[start] = 0
        updates = True
        for _ in range(nodes_count):
            if not updates:
                break
            updates = False
            for edge, node_a, node_b, weight in get_all_directed():
                if (
                    distances[node_a] != float("inf")
                    and distances[node_a] + weight < distances[node_b]
                ):
                    distances[node_b] = distances[node_a] + weight
                    used_edges[node_b] = edge
                    updates = True
        for _, node_a, node_b, weight in get_all_directed():
            if distances[node_a] != float("inf") and distances[node_a] + weight < distances[node_b]:
                return float("-inf"), None
        return distances, used_edges

    def shortest_path(self, start: str, end: str) -> tuple[int, Path]:
        # If any edge weight under 0, use bellman-ford
        if any([edge.weight < 0 for edge in self.edges]):
            logger.debug("starting bellman ford")
            distances, used_edges = self.bellman_ford(start)
            if isinstance(distances, float):
                return distances, None
            if isinstance(distances[end], float):
                return distances[end], None
            # Bellman ford found a distance, backtrack to find path
            path_nodes = [end]
            path_edges = []
            while start not in path_nodes:
                used_edge = used_edges[path_nodes[-1]]
                other_end = used_edge.other_end(path_nodes[-1])
                path_nodes.append(other_end)
                path_edges.append(used_edge)
            path = Path(list(reversed(path_edges)), list(reversed(path_nodes)))
            return distances[end], path
        # Else use state-space search using branch and bound.
        else:
            logger.debug("starting state space search")
            distance, path = self.state_space_search(end=end, nodes=self.edgemap.keys())
            return distance, path

    def bron_kerbosch(self) -> typing.List[typing.Set[typing.Any]]:
        """Finds all maximal cliques in the graph using the Bron-Kerbosch algorithm.

        This implementation uses a pivoting strategy to prune the search space,
        making it significantly more efficient for large, sparse graphs. A maximal
        clique is a clique that cannot be extended by adding another adjacent vertex.

        Returns:
            A list of sets, where each set contains the nodes forming a maximal clique.
        """
        cliques: typing.List[typing.Set[typing.Any]] = []
        r: typing.Set[typing.Any] = set()
        p: typing.Set[typing.Any] = set(self.edgemap.keys())
        x: typing.Set[typing.Any] = set()

        def bron_kerbosch_helper(
            r: typing.Set[typing.Any],
            p: typing.Set[typing.Any],
            x: typing.Set[typing.Any],
            cliques: typing.List[typing.Set[typing.Any]],
        ):
            """Recursive helper that performs the backtracking search with pivoting.

            Args:
                r: The current growing clique (Results).
                p: Potential candidates that can be added to the clique.
                x: Excluded vertices that have already been processed in this branch.
                cliques: The accumulator list where found maximal cliques are stored.
            """
            # If both P and X are empty, R is a maximal clique
            if not p and not x:
                cliques.append(r)
                return

            # If P is empty but X is not, this branch cannot yield a maximal clique
            if not p:
                return

            # Select a pivot to minimize the number of recursive calls.
            # The pivot is chosen from (P ∪ X) to maximize neighbors in P.
            pivot = max(p | x, key=lambda u: len(self.neigbouring_nodes(u) & p))

            # Iterate only through nodes in P that are NOT neighbors of the pivot
            for node in list(p - self.neigbouring_nodes(pivot)):
                bron_kerbosch_helper(
                    r | {node},
                    p & self.neigbouring_nodes(node),
                    x & self.neigbouring_nodes(node),
                    cliques,
                )
                # Move the node from 'Potential' to 'Excluded'
                p.remove(node)
                x.add(node)

        bron_kerbosch_helper(r, p, x, cliques)
        return cliques


def solve_task(sorted_edge_list, num_nodes):  # list of (distance, node1, node2) tuples

    edges_per_node = [0] * num_nodes
    chosen_edge_weights = []
    for i in range(num_nodes):
        while True:
            # Take last edge and check validity
            edge_weight, node1, node2 = sorted_edge_list.pop()
            if edges_per_node[node1] == 2 or edges_per_node[node2] == 2:
                continue  # Consider next
            chosen_edge_weights.append(edge_weight)
            edges_per_node[node1] += 1
            edges_per_node[node2] += 1
            break

    if len(chosen_edge_weights) != num_nodes:
        raise ValueError("not correct")
    total_weight = sum(chosen_edge_weights)
    return total_weight


def get_distance(coord1, coord2):
    dist = (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2
    return dist


def construct_graph(coordinates):
    graph = []
    for row_idx in range(len(coordinates)):
        row = []
        row_coord = coordinates[row_idx]
        for col_idx in range(len(coordinates)):
            col_coordinate = coordinates[col_idx]
            dist = get_distance(row_coord, col_coordinate)
            row.append(dist)
        graph.append(row)
    return graph


def solve_task_per_node(graph):
    num_nodes = len(graph)
    global_best = float("inf")
    for start_node in range(num_nodes):
        visited_nodes = [start_node]
        current_node = start_node

        chosen_paths = []
        for iteratie in range(num_nodes - 1):
            outgoing_edges = graph[current_node]
            next_node = -1
            next_node_value = float("inf")
            for target_node in range(num_nodes):
                if target_node in visited_nodes or target_node == current_node:
                    continue
                if outgoing_edges[target_node] < next_node_value:
                    next_node_value = outgoing_edges[target_node]
                    next_node = target_node
            current_node = next_node
            chosen_paths.append(next_node_value)
            visited_nodes.append(current_node)

        # Back to start node
        chosen_paths.append(graph[current_node][start_node])
        visited_nodes.append(start_node)
        logger.info(visited_nodes)
        current_best = sum(chosen_paths)
        if current_best < global_best:
            global_best = current_best

    return global_best


def construct_edge_list(graph):
    edge_list = []
    for row in range(len(coordinates)):
        for col in range(row + 1, len(coordinates)):
            edge_list.append((graph[row][col], row, col))

    return sorted(edge_list, reverse=True)


graph_matrix = []
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    if len(sys.argv) <= 1:
        # Read from standard input
        logger.info("No arguments, reading from standard input")
        input_lines = sys.stdin.readlines()
        output_filename = None
    else:
        # Read from file
        logger.info(f"Arguments provided, reading {sys.argv[1]}")
        with open(sys.argv[1], "r") as input_file:
            input_lines = input_file.readlines()
        output_filename = sys.argv[1].replace("invoer", "uitvoer.tvr")
        # Clear output file if it exists
        if os.path.exists(output_filename):
            os.remove(output_filename)

    starttime = datetime.datetime.now()

    num_entries = int(input_lines[0].strip())
    logger.info(f"Number of entries: {num_entries}")

    line_idx = 1
    for entry in range(num_entries):
        logger.info(f"Reading entry {entry+1} out of {num_entries}")

        # Start of parsing
        num_hutten = int(input_lines[line_idx].strip())
        line_idx += 1

        coordinates = []
        for i in range(num_hutten):
            x, y = tuple(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1
            coordinates.append((x, y))

        # Fill matrix
        graph_matrix = construct_graph(coordinates)

        # Start of processing
        sorted_edge_list = construct_edge_list(graph_matrix)
        edges = []
        for edge_weight, node1, node2 in sorted_edge_list:
            edges.append(Edge(node1, node2, edge_weight, bidirectional=False))
            edges.append(Edge(node2, node1, edge_weight, bidirectional=False))

        graph = Graph(edges=edges)
        # value = solve_task(sorted_edge_list, num_hutten)
        value = graph.shortest_path(0, 0)[0]
        # value = solve_task_per_node(graph)
        solution_str = f"{entry + 1} {value}"

        # Write to stdout
        print(solution_str, flush=True)
        # Write to output file
        if output_filename:
            with open(output_filename, "a") as f:
                f.write(solution_str + "\n")

    logger.info(f"Done. Time elapsed: {datetime.datetime.now() - starttime}")
