import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import StagedActivation

from route_66.agent import CarAgent, TrafficLight


def get_average_velocity(model):
    """
    Gets the total average velocity over all the agents

    :param model: The model (environment) where the agents exist

    :return: The total average velocity over all the agents
    """
    df = model.datacollector.get_agent_vars_dataframe()
    df.reset_index(inplace=True)
    velocities = df["Velocity"]

    return velocities.mean()


def get_standard_deviation_velocity(model):
    """
    Gets the total standard deviation of the velocity over all agents

    :param model: The model (environment) where the agents exist

    :return: The total standard deviation over all agents
    """
    df = model.datacollector.get_agent_vars_dataframe()
    df.reset_index(inplace=True)
    velocities = df["Velocity"]

    return velocities.std()


class RoadModel(Model):
    """
    A model with a number of cars, Nagel-Schreckenberg
    """

    def __init__(self, N, length=100, lanes=1, timer=3):
        self.num_agents = N
        self.grid = SingleGrid(length, lanes, torus=True)
        model_stages = ["acceleration", "braking", "randomisation", "move", "delete"]
        self.schedule = StagedActivation(self, stage_list=model_stages)

        # Create agent
        for i in range(self.num_agents):
            agent = CarAgent(i, self, False)
            # Add to schedule
            self.schedule.add(agent)
            # Add to grid (randomly)
            self.grid.position_agent(agent)

        # Add the traffic light
        self.traffic_light = TrafficLight(0, self, timer, 20, 20)
        self.average_velocity = CarAgent.init_velocity
        self.datacollector = DataCollector(agent_reporters={
            "Position": "pos",
            "Velocity": "velocity"},
            model_reporters={
                "Average Velocity": "average_velocity",
                "Amount of cars": "agent_count"})

        self.running = True

    def step(self):
        """
        The model takes a new step and updates
        """
        # Calculate amount of agents
        self.agent_count = len(self.schedule.agents)
        # Calculate average velocity
        self.average_velocity = np.mean([a.velocity for a in self.schedule.agents])
        # Collect data
        self.datacollector.collect(self)
        # Run a step of the traffic light
        self.traffic_light.step()
        # Run next step
        self.schedule.step()

    def add_agent(self, label, x_corr):
        """
        Adds an agent to the scheduler and model on a particular coordinate

        :param label: The label of the agents that gets created
        :param x_corr: The x-coordinate of where the agent will be spawned
        """
        # Create agent
        agent = CarAgent(label, self, True)
        # Add to schedule
        self.schedule.add(agent)
        # Add to grid on a certain position
        self.grid.position_agent(agent, x_corr, 0)

    def delete_agent(self, agent):
        """
        Deletes an agent from the scheduler and model

        :param agent: The agents that gets deleted
        """
        # remove from schedule
        self.schedule.remove(agent)
        # remove from grid
        self.grid.remove_agent(agent)
