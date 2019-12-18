import matplotlib.pyplot as plt
import seaborn as sns
from mesa.batchrunner import BatchRunner

from route_66.agent import CarAgent
from route_66.model import RoadModel, get_average_velocity, get_standard_deviation_velocity
from route_66.model import get_on_ramp_queue, get_waiting_queue


def run_batch(N=[35], timer=[2], iterations=5, max_steps=100):
    """
    Runs the simulation for every combination of N and timer
    N is the number of Cars on the road
    Timer is the amount of seconds the traffic light will wait to let agents through

    :param N: List of each number of initial cars on the road
    :param timer: List of each timing that needs to be simulated
    :param iterations: Integer of the amount of times every single combination needs to be repeated
    :param max_steps: Maximum amount of steps each simulation will run

    :return: DataFrame with the Average Velocity and Standard Deviation of the velocity for every combination
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
        max_steps=max_steps,
        model_reporters={
            "Average Velocity": get_average_velocity,   # Average velocity per simulation
            "Standard Deviation": get_standard_deviation_velocity,
            "On Ramp Queue": get_on_ramp_queue,
            "Waiting Queue": get_waiting_queue})

    batch_run.run_all()  # Run all simulations
    run_data = batch_run.get_model_vars_dataframe()  # Get DataFrame with collected data
    return run_data
