from mesa.batchrunner import BatchRunner
from route_66.model import RoadModel, get_average_velocity
import matplotlib.pyplot as plt
import numpy as np

# https://github.com/Casper-Smet/intro-to-agents/blob/master/batch_run.py


def run_batch():
    fixed_params = {
        "length": 100,
        "lanes": 1
    }

    variable_params = {"N": [35, 50, 80],
                       "timer": range(2, 10)}

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

    run_data = batch_run.get_model_vars_dataframe().groupby("N")
    groups = [run_data.get_group(x) for x in run_data.groups]

    fig, ax = plt.subplots()

    ns = [35, 50, 80]
    for group, n in zip(groups, ns):
        ax.scatter(np.arange(0, 40), group["Average Velocity"], label=n)

    plt.legend()
    plt.xlabel("Run")
    plt.ylabel("Average Velocity")

    plt.show()
