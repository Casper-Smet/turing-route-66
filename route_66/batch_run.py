from mesa.batchrunner import BatchRunner
from route_66.model import RoadModel, get_average_velocity
from route_66.agent import CarAgent
import matplotlib.pyplot as plt
import numpy as np

# https://github.com/Casper-Smet/intro-to-agents/blob/master/batch_run.py


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
            "Average Velocity": get_average_velocity})  # Average velocity per simulation

    batch_run.run_all()  # Run all simulations
    run_data = batch_run.get_model_vars_dataframe()  # Get DataFrame with collected data
    return run_data


def plot_batch(N=[35], timer=[2]):
    """
    Plots each combination of N and timer.
    Each combination has its own coloured dot.
    Each combination is run for several iterations, thus several dots.
    """
    run_data = run_batch(N=N, timer=timer)
    df_N_groups = run_data.groupby("N")
    N_groups = [df_N_groups.get_group(x) for x in df_N_groups.groups]

    for N_group, N_agents in zip(N_groups, N):  # Each individual N of agents
        df_timer_groups = N_group.groupby("timer")
        timer_groups = [df_timer_groups.get_group(x) for x in df_timer_groups.groups]

        for timer_group, seconds in zip(timer_groups, timer):  # Each individual amount of seconds within each individual N of agents
            plt.scatter(np.arange(timer_group.shape[0]), timer_group["Average Velocity"], label=f"Agents: {N_agents}, Timer: {seconds}")

    plt.legend()
    plt.xlabel("Iteration for given parameter")
    plt.ylabel("Average Velocity")
    plt.xlim(-0.5, timer_group.shape[0] - 0.5)
    plt.ylim(0, CarAgent.max_velocity)

    plt.show()
