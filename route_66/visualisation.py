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

    _, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(velocities["Position"], velocities["Step"], marker="s", color="black", s=10, zorder=1)

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


def plot_queues(N=[10, 25, 35], timer=[0, 1, 2, 4, 6], iterations=20):
    run_data = run_batch(N=N, timer=timer, iterations=iterations)

    sns.set("paper")
    _, ax = plt.subplots()
    sns.scatterplot("timer", "Waiting Queue", data=run_data, label="Waiting Queue, 2 cars per step", ax=ax)
    sns.scatterplot("timer", "On Ramp Queue", hue="N", data=run_data, ax=ax)
