
from mesa import Model

class RoadModel(Model):
    """A model with a number of cars, Nagel-Schreckenberg"""
    def __init__(self, N, length, lanes=1):
        self.num_agents = N 
        # GRID tbd
        # Time tbd

    def step(self):
        pass