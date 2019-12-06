import matplotlib.pyplot as plt
import numpy as np

from route_66.model import RoadModel


def plot(steps, N, length=60, lanes=1):
    model = RoadModel(N, length=length, lanes=lanes)
    for _ in range(steps):
        model.step()

    velocities = model.datacollector.get_agent_vars_dataframe()
    velocities.reset_index(inplace=True)
    velocities["Position"] = velocities['Position'].apply(lambda x: x[0] + 0.5)

    fig, ax = plt.subplots()
    ax.scatter(velocities["Position"], velocities["Step"], marker="s", color="black")

    # ax.invert_yaxis()

    ax.set_xlabel("Position on the road")
    ax.set_ylabel(f"Time: 0 to {steps}")
    ax.set_xlim(0, length)
    ax.set_ylim(0, steps)

    plt.show()
