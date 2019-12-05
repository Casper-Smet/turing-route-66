from mesa import Agent
import mesa.space


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
        """If the distance between an agent and the agent in front of it is smaller than the velocity
        the velocity is reduced to the number of emtpy cells in front of the car"""
        x, y = self.pos
        for i in range(1, self.velocity + 1):
            x0, y0 = self.model.grid.torus_adj((x + i, y))
            if not self.model.grid.is_cell_empty((x0, y0)):
                self.velocity = i - 1
                break

        return self.velocity

    def randomisation(self):
        """If an agent's velocity is greater than 1, 
        it may slow down by one unit of velocity randomly with a probability of CarAgent.p"""
        if self.velocity > 1:
            if self.random.random() < CarAgent.p:
                self.velocity -= 1

        return self.velocity

    def move(self):
        """The agent is moved forward the number of cells equal to their velocity"""
        x, y = self.pos
        new_pos = (x + self.velocity, y)
        new_pos = self.model.grid.torus_adj(new_pos)

        self.model.grid.move_agent(self, new_pos)
