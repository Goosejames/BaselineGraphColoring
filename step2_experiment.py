# CT421 Assignment 1
# Step 2 Experiment
# Roan Elwood (22424162)
# James Goose (22403502)

import matplotlib.pyplot as plt
from Graph_Colouring import (
    SimConfig,
    build_random_geometric_graph,
    assign_initial_colours,
    run_colouring,
)

# Number of runs per experiment
RUNS_PER_SETTING = 25

# Colour values (range) that we'll test
COLOUR_VALUES = [3,4,5,6,7,8,9,10]


def run_colour_experiment():
    base_cfg = SimConfig()
    avg_steps = []
    print("Running step 2 experiment\n")
    # Test each colour count
    for colours in COLOUR_VALUES:
        steps_list = []

        # run multiple simulations for each colour count to get an avg
        for run in range(RUNS_PER_SETTING):
            cfg = SimConfig(
                node_count=base_cfg.node_count,
                radius=base_cfg.radius,
                colour_count=colours,
                max_steps=base_cfg.max_steps,
                seed=base_cfg.seed + run
            )
            # build random geometric graph
            graph, _ = build_random_geometric_graph(cfg)
            # Assign initial random colours
            initial = assign_initial_colours(graph, cfg.colour_count, cfg.seed)
            _, history = run_colouring(graph, initial, cfg)
            steps_taken = len(history) - 1 # minus the initial state
            steps_list.append(steps_taken)

        avg = sum(steps_list) / len(steps_list) # average 
        avg_steps.append(avg)

        print(f"Colours = {colours}   Average Steps = {avg:.2f}")

    return avg_steps

#plot number of colours vs average steps to convergence
def plot_results(colours, avg_steps):
    plt.figure(figsize=(10,5))
    plt.plot(colours, avg_steps, marker="o")
    plt.xlabel("Number of Colours")
    plt.ylabel("Average Steps to Convergence")
    plt.title("Effect of Colour Count on Graph Colouring Convergence")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    avg_steps = run_colour_experiment()
    plot_results(COLOUR_VALUES, avg_steps)


if __name__ == "__main__":
    main()