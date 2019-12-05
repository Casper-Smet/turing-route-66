from mesa.space import SingleGrid
from mesa.time import StagedActivation
from mesa import Model

class RoadModel(Model):
    """A model with a number of cars, Nagel-Schreckenberg"""
    def __init__(self, N, length, lanes=1):
        self.num_agents = N 
        self.grid = SingleGrid(length, lanes, True)
        self.schedule = StagedActivation(self)

    def step(self):
        pass