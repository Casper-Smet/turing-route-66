from mesa.batchrunner import BatchRunner
from route_66.model import RoadModel, get_average_velocity
from route_66.agent import CarAgent
import matplotlib.pyplot as plt
import numpy as np

# https://github.com/Casper-Smet/intro-to-agents/blob/master/batch_run.py


def run_batch(N=[35], timer=[2]):
    fixed_params = {
        "length": 100,
        "lanes": 1
    }

    variable_params = {"N": N,
                       "timer": timer}

    # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
    batch_run = BatchRunner(
        RoadModel,
        variable_params,
        fixed_params,
        iterations=5,
        max_steps=100,
        model_reporters={
            "Average Velocity": get_average_velocity})

    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    run_data_gb = run_data.groupby("N")

    groups = [run_data_gb.get_group(x) for x in run_data_gb.groups]
    for group, n in zip(groups, N):
        plt.scatter(np.arange(0, group.shape[0]), group["Average Velocity"], label=n)

    plt.legend()
    plt.xlabel("Run")
    plt.ylabel("Average Velocity")
    plt.xlim(0, group.shape[0])
    plt.ylim(0, CarAgent.max_velocity)

    print(run_data.head())
    plt.show()
