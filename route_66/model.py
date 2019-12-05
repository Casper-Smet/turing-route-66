from mesa.space import SingleGrid
from mesa import Model

class RoadModel(Model):
    """A model with a number of cars, Nagel-Schreckenberg"""
    def __init__(self, N, length, lanes=1):
        self.num_agents = N 
        self.grid = SingleGrid(length, lanes, True)
        # Time tbd

    def step(self):
        pass