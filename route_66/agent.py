from mesa import Agent

class CarAgent(Agent):
    """An agent with a velocity of 1-5 and a position. Random initial velocity"""
    init_velocity = 1
    
    def __init__(self, unique_id, model):
        super.__init__(unique_id, model)
        self.velocity = CarAgent.init_velocity

    def acceleration(self):
        pass

    def braking(self):
        pass

    def randomisation(self):
        pass

    def move(self):
        pass