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
    
    def other_end(self, node:str) -> str:
        if node == self.node_a:
            return self.node_b
        return self.node_a

    def __hash__(self) -> int:
        return hash((self.node_a, self.node_b, self.weight, self.bidirectional, self.mandatory))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False
        return self.node_a == other.node_a and self.node_b == other.node_b and self.weight == other.weight and self.bidirectional == other.bidirectional and self.mandatory == other.mandatory
    
    def __repr__(self) -> str:
        return f'{self.node_a} -> {self.node_b} ({self.weight})'
    
@dataclasses.dataclass
class Path:
    edges: list[Edge]
    nodes: list[str]

    def distance(self) -> int:
        return sum([edge.weight for edge in self.edges])
    
    def min_est_distance(self) -> int:
        return self.distance()
    
    def __lt__(self, other: typing.Self) -> bool:
        return self.min_est_distance() < other.min_est_distance()
    
    def __repr__(self) -> str:
        return ', '.join([f'{self.nodes[i-1]} -> {self.nodes[i]} ({self.edges[i-1].weight})' for i in range(1, len(self.nodes))])
    
class Graph:
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        self.edgemap = self.build_edge_map(edges)

    def __repr__(self) -> str:
        return ', '.join(map(str, [edge for edge in self.edges]))

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
    
    def state_space_search(self, end: str, frontier: tuple[float, list[Path]] = None) -> tuple[int, Path]:
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
            frontier = [(0, Path([], [start]))]
        min_distance=float('inf')
        optimal_path = None
        state_memo = dict()
        while(frontier):
            _, most_promising_path = heapq.heappop(frontier)
            if most_promising_path.min_est_distance() >= min_distance:
                continue
            state = (frozenset(most_promising_path.edges), most_promising_path.nodes[-1])
            distance = most_promising_path.distance()
            if state in state_memo and state_memo[state] <= distance:
                continue
            state_memo[state] = distance
            if most_promising_path.nodes[-1] == end:
                if all([mandatory_edge in most_promising_path.edges for mandatory_edge in self.edges if mandatory_edge.mandatory]):
                    if distance < min_distance:
                        min_distance = distance
                        optimal_path = most_promising_path
                    continue
            for edge in self.edgemap[most_promising_path.nodes[-1]]:
                next_path = Path(most_promising_path.edges + [edge], most_promising_path.nodes + [edge.other_end(most_promising_path.nodes[-1])])
                heapq.heappush(frontier, (next_path.min_est_distance(), next_path))
        return min_distance, optimal_path
    
    def bellman_ford(self, start:str) -> tuple[typing.Union[dict[str, float], float], typing.Union[dict[str, Edge], None]]:
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
        distances = {node: float('inf') for node in self.get_nodes()}
        used_edges = {node: None for node in self.get_nodes()}
        distances[start] = 0
        updates = True
        for _ in range(nodes_count):
            if not updates:
                break
            updates = False
            for edge, node_a, node_b, weight in get_all_directed():
                if distances[node_a] != float('inf') and distances[node_a] + weight < distances[node_b]:
                    distances[node_b] = distances[node_a] + weight
                    used_edges[node_b] = edge
                    updates = True
        for _, node_a, node_b, weight in get_all_directed():
            if distances[node_a] != float('inf') and distances[node_a] + weight < distances[node_b]:
                return float('-inf'), None
        return distances, used_edges

    def shortest_path(self, start: str, end: str) -> tuple[int, Path]:
        # If any edge weight under 0, use bellman-ford
        if any([edge.weight < 0 for edge in self.edges]):
            logger.debug('starting bellman ford')
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
            logger.debug('starting state space search')
            distance, path =  self.state_space_search(end=end)
            return distance, path
        
    def bron_kerbosh(self):
        clicques = []
        r = set()
        p = set(self.edgemap.keys())
        x = set()

        def bron_kerbosch_helper(r, p, x, cliques):
            if not p and not x:
                cliques.append(r)
                return
            
            if not p:
                return
            
            pivot = max(p | x, key=lambda u: len(self.neigbouring_nodes(u) & p))

            for node in list(p - self.neigbouring_nodes(pivot)):
                bron_kerbosch_helper(r | {node},
                                     p & self.neigbouring_nodes(node),
                                     x & self.neigbouring_nodes(node),
                                     cliques)
                p.remove(node)
                x.add(node)

        bron_kerbosch_helper(r, p, x, clicques)
        return clicques

def process(graph):
    change = True
    old_deadends = set()
    deadends = set()
    while(change):
        old_deadends = set(deadends)
        for edge in graph.edges:
            for node in edge.start_nodes():
                start_node = node
                end_node = edge.other_end(node)
                directed = (start_node, end_node)
                if directed in deadends:
                    continue
                possible_edges = graph.edgemap[end_node]
                only_deadends = True
                for possible_edge in possible_edges:
                    possible_edge_start_node = end_node
                    possible_edge_end_node = possible_edge.other_end(possible_edge_start_node)
                    if possible_edge_end_node == start_node:
                        continue
                    possible_edge_directed = (possible_edge_start_node, possible_edge_end_node)
                    if possible_edge_directed not in deadends:
                        only_deadends = False
                        continue
                if only_deadends:
                    deadends.add(directed)
        if old_deadends == deadends:
            break
    if len(deadends) == 0:
        return "geen"
    output = ''
    for deadend in sorted(deadends):
        output += f'({deadend[0]},{deadend[1]}) '
    return output.strip()


def yield_neighbors(
    matrix: typing.Sequence[typing.Sequence[int]], 
    i: int, 
    j: int, 
    include_diagonals: bool = False,
    exclude_matrix: list[list[bool]] = None
) -> typing.Generator[int, None, None]:
    """
    Yields adjacent values from a 2D matrix with type safety.
    
    Args:
        matrix: A 2D sequence (list of lists) containing elements of type T.
        i: The row index.
        j: The column index.
        include_diagonals: Whether to include the 4 diagonal neighbors.
        exclude_matrix: Whether to skip a certain value

    Yields:
        Elements of type int from the adjacent cells.
    """
    # Defensive check: Ensure matrix is not empty
    if not matrix or not matrix[0]:
        return

    rows: int = len(matrix)
    cols: int = len(matrix[0])

    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            
            # Manhattan distance logic for orthogonal neighbors
            if not include_diagonals and abs(di) + abs(dj) > 1:
                continue

            ni, nj = i + di, j + dj            
            
            if 0 <= ni < rows and 0 <= nj < cols:
                if exclude_matrix and exclude_matrix[ni][nj]:
                    continue
                yield matrix[ni][nj]

def endoints(matrix):
    endpoint_matrix = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i_index, row in enumerate(matrix):
        for j_index, value in enumerate(row):
            adjacent = list(yield_neighbors(matrix, i_index, j_index, False))
            if adjacent.count(value) <= 1:
                endpoint_matrix[i_index][j_index] = True
    return endpoint_matrix

def build_graph(matrix, endpoints_matrix):
    adjacent_dict = collections.defaultdict(set)
    max_val = 0
    for i_index, row in enumerate(matrix):
        for j_index, value in enumerate(row):
            for adjacent_value in yield_neighbors(matrix, i_index, j_index, exclude_matrix=endpoints_matrix):
                adjacent_dict[value].add(adjacent_value)
            if value > max_val:
                max_val = value
    logger.debug(f'{adjacent_dict=}, {max_val=}')
    edges = []
    for i in range(1, max_val + 1):
        for j in range(1, max_val + 1):
            if i == j:
                continue
            if j in adjacent_dict[i] or i in adjacent_dict[j]:
                continue
            edge = Edge(i, j, 1)
            edges.append(edge)
    return Graph(edges)

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
        height, width = tuple(map(int,input_lines[line_index].strip().split()))
        logger.info(f'{height=}, {width=}')
        line_index += 1
        matrix = []
        for j in range(height):
            row = tuple(map(int, input_lines[line_index].strip().split()))
            matrix.append(row)
            line_index += 1
        endpoints_matrix = endoints(matrix)
        graph = build_graph(matrix, endpoints_matrix)
        logger.debug(f'{endpoints_matrix=}, {graph=}')
        # End of parsing

        # Start of processing
        max_clicques = graph.bron_kerbosh()
        logger.debug(f'{max_clicques}')
        output_line = max(max((len(clicque) for clicque in max_clicques)),1)
        logger.debug(f'Output: {i + 1} {output_line}')
        print(f'{i + 1} {output_line}', flush=True)
        # End of processing
            
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')