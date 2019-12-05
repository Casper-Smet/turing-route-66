from agent import CarAgent

from mesa.space import SingleGrid
from mesa.time import StagedActivation
from mesa import Model

class RoadModel(Model):
    """A model with a number of cars, Nagel-Schreckenberg"""
    def __init__(self, N, length, lanes=1):
        self.num_agents = N 
        self.grid = SingleGrid(length, lanes, True)
        model_stages = ["acceleration", "braking", "randomisation", "move"]
        self.schedule = StagedActivation(self, stage_list=model_stages)


        # Create agent
        for i in range(self.num_agents):
            a = CarAgent(i, self)
            # Add to schedule
            self.schedule.add(a)
            # Add to grid (randomly)
            self.grid.position_agent(a)


    def step(self):
        self.schedule.step()