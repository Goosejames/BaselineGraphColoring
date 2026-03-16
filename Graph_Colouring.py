# CT421 Assignemnt 1
# Graph Colouring
# Roan Elwood (22424162)
# James Goose (22403502)

import random
from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx


@dataclass(frozen=True)
class SimConfig:
    # Simulation parameters
    node_count: int = 60
    radius: float = 0.22
    colour_count: int = 8
    max_steps: int = 400
    seed: int = 7


def build_random_geometric_graph(cfg: SimConfig) -> tuple[nx.Graph, dict[int, tuple[float, float]]]:
    # Place nodes randomly in the unit square and connect if within radius.
    rng = random.Random(cfg.seed)
    positions = {i: (rng.random(), rng.random()) for i in range(cfg.node_count)}
    graph = nx.random_geometric_graph(cfg.node_count, cfg.radius, pos=positions)
    return graph, positions


def assign_initial_colours(graph: nx.Graph, colour_count: int, seed: int) -> dict[int, int]:
    # Start with a random colour assignment.
    rng = random.Random(seed)
    return {node: rng.randrange(colour_count) for node in graph.nodes()}


def edge_conflict_count(graph: nx.Graph, colours: dict[int, int]) -> int:
    # Count edges whose endpoints share the same colour.
    return sum(1 for u, v in graph.edges() if colours[u] == colours[v])


def available_colours(node: int, graph: nx.Graph, colours: dict[int, int], colour_count: int) -> list[int]:
    # Collect neighbour colours and return the remaining options.
    used = {colours[nb] for nb in graph.neighbors(node)}
    return [c for c in range(colour_count) if c not in used]


def update_step(graph: nx.Graph, colours: dict[int, int], colour_count: int, rng: random.Random) -> dict[int, int]:
    # Apply one local update step to resolve conflicts.
    next_colours = colours.copy()

    for node in graph.nodes():
        # only adjust nodes that are currently in conflict
        in_conflict = any(colours[node] == colours[nb] for nb in graph.neighbors(node))
        if not in_conflict:
            continue

        choices = available_colours(node, graph, colours, colour_count)
        if choices:
            next_colours[node] = rng.choice(choices)
        else:
            next_colours[node] = rng.randrange(colour_count)

    return next_colours


def run_colouring(graph: nx.Graph, initial: dict[int, int], cfg: SimConfig) -> tuple[dict[int, int], list[int]]:
    # Iterate updates until no conflicts or max steps reached.
    rng = random.Random(cfg.seed + 101)
    colours = initial.copy()
    history = [edge_conflict_count(graph, colours)]

    for _ in range(cfg.max_steps):
        if history[-1] == 0:
            break  # stop early if solved
        colours = update_step(graph, colours, cfg.colour_count, rng)
        history.append(edge_conflict_count(graph, colours))

    return colours, history


def describe_graph(graph: nx.Graph) -> None:
    # Print basic graph statistics.
    degrees = dict(graph.degree())
    avg_degree = sum(degrees.values()) / max(1, graph.number_of_nodes())
    print("Graph created:")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    print(f"Avg degree: {avg_degree:.2f}")


def plot_conflicts(history: list[int], cfg: SimConfig) -> None:
    # Plot conflicts over time to visualize convergence.
    plt.figure(figsize=(10, 5))
    plt.plot(history, color="tab:blue", label="Conflicts")
    plt.xlabel("Step")
    plt.ylabel("Edge conflicts")
    plt.title(
        "Random Geometric Graph Colouring\n"
        f"N={cfg.node_count}, r={cfg.radius}, colours={cfg.colour_count}"
    )
    plt.ylim(bottom=0)
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_colouring(graph: nx.Graph, pos: dict[int, tuple[float, float]], colours: dict[int, int], cfg: SimConfig) -> None:
    # Visualize the final colouring on the geometric layout.
    plt.figure(figsize=(8, 8))
    node_vals = [colours[node] for node in graph.nodes()]

    nodes = nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_vals,
        cmap=plt.cm.tab10,
        node_size=260,
    )
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=8)

    cbar = plt.colorbar(nodes)
    cbar.set_label("Colour ID")
    if cfg.colour_count > 1:
        nodes.set_clim(0, cfg.colour_count - 1)

    plt.title("Final Colouring (Random Geometric Graph)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main() -> None:
    # Orchestrate graph creation, simulation, and plots.
    cfg = SimConfig()
    graph, positions = build_random_geometric_graph(cfg)
    describe_graph(graph)

    initial_colours = assign_initial_colours(graph, cfg.colour_count, cfg.seed)
    final_colours, history = run_colouring(graph, initial_colours, cfg)

    print(f"Initial conflicts: {history[0]}")
    print(f"Final conflicts: {history[-1]}")
    print(f"Steps taken: {len(history) - 1}")

    plot_conflicts(history, cfg)
    plot_colouring(graph, positions, final_colours, cfg)


if __name__ == "__main__":
    # Entry point for script execution.
    main()