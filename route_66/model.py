from route_66.agent import CarAgent, TrafficLight

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import StagedActivation
from mesa.datacollection import DataCollector
import numpy as np


class RoadModel(Model):
    """A model with a number of cars, Nagel-Schreckenberg"""

    def __init__(self, N, length=100, lanes=1):
        self.num_agents = N
        self.grid = SingleGrid(length, lanes, torus=True)
        model_stages = ["acceleration", "braking", "randomisation", "move"]
        self.schedule = StagedActivation(self, stage_list=model_stages)

        # Create agent
        for i in range(self.num_agents):
            agent = CarAgent(i, self)
            # Add to schedule
            self.schedule.add(agent)
            # Add to grid (randomly)
            self.grid.position_agent(agent)

        # Add the traffic light
        self.traffic_light = TrafficLight(0, self, 3, 2)
        self.average_velocity = CarAgent.init_velocity
        self.datacollector = DataCollector(agent_reporters={
            "Position": "pos",
            "Velocity": "velocity"},
            model_reporters={
            "Average Velocity": "average_velocity"})

        self.running = True

    def step(self):
        # Calculate average velocity
        self.average_velocity = np.mean([a.velocity for a in self.schedule.agents])
        # Collect data
        self.datacollector.collect(self)
        # Run next step
        self.schedule.step()

    def add_agent(self, label, x_corr):
        """Adds an agent to the scheduler and model on a particular coordinate"""
        # Create agent
        agent = CarAgent(label, self)
        # Add to schedule
        self.schedule.add(agent)
        # Add to grid (randomly)
        self.grid.position_agent(agent, x_corr, 0)
