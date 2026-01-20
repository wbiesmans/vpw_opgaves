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

    def get_nodes(self) -> set[str]:
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.node_a)
            nodes.add(edge.node_b)
        return nodes

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

def process(graph, start, end):
    result, path = graph.shortest_path(start, end)
    logger.info(f'{result=}, {path=}')
    if result == float('inf'):
        result = 'plus oneindig'
    if result == float('-inf'):
        result = 'min oneindig'
    return result

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
        number_of_nodes, number_of_edges = tuple(map(int, input_lines[line_index].strip().split()))
        logger.info(f'{number_of_nodes=}, {number_of_edges=}')
        edges = []
        for j in range(number_of_edges):
            node_a, node_b, weight = tuple(input_lines[line_index+1+j].strip().split())
            weight = int(weight)
            edges.append(Edge(node_a, node_b, weight, bidirectional=False))
        graph = Graph(edges=edges)
        start = str(1)
        end = str(number_of_nodes)
        line_index += number_of_edges + 1
        # End of parsing

        # Start of processing
        output_line = process(graph, start, end)
        print(f'{i + 1} {output_line}')
        # End of processing
    i = 1
            
    logger.info(f'Done. Time elapsed: {datetime.datetime.now() - starttime}')