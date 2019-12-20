import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from route_66.agent import CarAgent
from route_66.batch_run import run_batch
from route_66.model import RoadModel


def plot_simulation(steps, N, length=100, lanes=1, p=0.5, grid=False):
    """Visualises the development of traffic throughput

    :param steps: Integer of the amount of steps the simulation needs to run
    :param N: List of each number of initial cars on the road
    :param length: Integer of the length of the road
    :param lanes: The amount of lanes the road has
    :param p: The probability a car will decrease speed by one
    :param grid: Boolean to show the grid on the plot or not

    :return:  No return but shows the plot instead
    """
    assert N < length, "It is not possible to have more cars than cells"
    model = RoadModel(N, length=length, lanes=lanes)
    CarAgent.p = p

    for _ in range(steps):
        model.step()

    velocities = model.datacollector.get_agent_vars_dataframe()
    velocities.reset_index(inplace=True)
    velocities["Position"] = velocities['Position'].apply(lambda x: x[0] + 0.5)
    velocities["Step"] = velocities["Step"].apply(lambda x: x + 0.5)

    sns.set("poster")
    _, ax = plt.subplots(figsize=(8, 8))
    sns.scatterplot(velocities["Position"], velocities["Step"], marker="s", color="black", s=10, zorder=1, ax=ax)

    if grid:
        spacing = np.arange(0, steps)
        plt.hlines(spacing, length, 0, color="grey", alpha=0.3, zorder=0)
        plt.vlines(spacing, steps, 0, color="grey", alpha=0.3, zorder=0)

    plt.title(f"Simulation of {N} cars during {steps} time steps \non a continuous road of {length} cells long.")
    ax.set_xlabel("Position on the road")
    ax.set_ylabel(f"Time: 0 to {steps}")
    ax.set_xlim(0, length)
    ax.set_ylim(0, steps)

    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.show()


def plot_batch_run(N=[35], timer=[2], iterations=5, max_steps=100):
    """
    Plots each combination of N and timer.
    Each combination has its own coloured dot.
    Each combination is run for several iterations, thus several dots.

    :param N: List of each number of initial cars on the road
    :param timer: List of each timing that needs to be simulated
    :param iterations: Integer of the amount of times every single combination needs to be repeated

    :return: the DataFrame associated with the batch plot
    """
    run_data = run_batch(N=N, timer=timer, iterations=iterations, max_steps=max_steps)
    run_data["Run"] += 1  # Run starts now at 1, better for plot limits

    sns.set("poster")
    _, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(x="timer", y="Average Velocity", hue="N", data=run_data, ax=ax)

    ax.set_title(f"{run_data.shape[0]} runs of the simulation using multiple combinations of 'N' and 'timer'\nEach simulation will run for {max_steps} steps.")
    ax.set_xlabel(f"Different timers: {timer}")
    ax.set_ylabel("Average Velocity")
    ax.set_xlim(-0.5, len(timer) - 0.5)
    ax.set_ylim(0, CarAgent.max_velocity)

    plt.legend()
    plt.show()

    # Returns the same data as used in the plot, run_batch() could be used if the data does not need to be the same as plot
    return run_data
