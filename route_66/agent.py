from mesa import Agent


class CarAgent(Agent):
    """An agent with a velocity of 1-5 and a position. Random initial velocity"""
    init_velocity = 1
    max_velocity = 5
    p = 0.5

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.velocity = CarAgent.init_velocity

    def acceleration(self):
        """Increases velocity by one unit if it is smaller than CarAgent.max_velocity"""
        if self.velocity < CarAgent.max_velocity:
            self.velocity += 1

        return self.velocity

    def braking(self):
        pass

    def randomisation(self):
        """If an agent's velocity is greater than 1, 
        it may slow down by one unit of velocity randomly with a probability of CarAgent.p"""
        if self.velocity > 1:
            if self.random.random() < CarAgent.p:
                self.velocity -= 1

        return self.velocity

    def move(self):
        pass
