import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mesa.batchrunner import BatchRunner

from route_66.agent import CarAgent
from route_66.model import RoadModel, get_average_velocity, get_standard_deviation_velocity


def run_batch(N=[35], timer=[2], iterations=5):
    """
    Runs the simulation for every combination of N and timer
    N is the number of Cars on the road
    Timer is the amount of seconds the traffic light will wait to let agents through

    Returns DataFrame with all the collected data of all the simulations
    """
    # Parameters that won't be changed during any of the iterations
    fixed_params = {
        "length": 100,
        "lanes": 1
    }

    # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
    variable_params = {"N": N,
                       "timer": timer}

    batch_run = BatchRunner(
        RoadModel,
        variable_params,
        fixed_params,
        iterations=iterations,  # Iterations per combination of parameters
        max_steps=100,
        model_reporters={
            "Average Velocity": get_average_velocity,
            "Standard Deviation": get_standard_deviation_velocity})  # Average velocity per simulation

    batch_run.run_all()  # Run all simulations
    run_data = batch_run.get_model_vars_dataframe()  # Get DataFrame with collected data
    return run_data


def plot_batch(N=[35], timer=[2], iterations=5):
    """
    Plots each combination of N and timer.
    Each combination has its own coloured dot.
    Each combination is run for several iterations, thus several dots.
    """
    run_data = run_batch(N=N, timer=timer, iterations=iterations)
    run_data["Run"] += 1  # Run starts now at 1, better for plot limits

    # ax = sns.scatterplot("Run", "Average Velocity", data=run_data, size="N", hue="timer", palette="Set1")
    ax = sns.boxplot(x="timer", y="Average Velocity", hue="N", data=run_data)

    ax.set_title(f"{run_data.shape[0]} runs of the simulation using multiple combinations of 'N' and 'timer'")
    ax.set_xlabel(f"Different timers: {timer}")
    ax.set_ylabel("Average Velocity")
    ax.set_xlim(-0.5, len(timer) - 0.5)
    ax.set_ylim(0, CarAgent.max_velocity)

    plt.legend()
    plt.show()
