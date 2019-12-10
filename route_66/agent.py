from mesa import Agent
import mesa.space


class CarAgent(Agent):
    """An agent with a velocity of 1-5 and a position. Random initial velocity"""
    init_velocity = 5
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


class TrafficLight(object):
    merge_begin = 10
    merge_end = 30

    def __init__(self, unique_id, model, timer, ca):
        self.unique_id = unique_id
        self.model = model
        self.current_car_id = 0

        self.wait_queue = []
        self.on_ramp_queue = []

        self.timer = timer
        self.counter = 0
        self.cars_amount = ca

    def step(self):
        """The traffic light"""
        if self.counter == self.timer:
            # let cars through
            self.counter = 0
            # update the queues
            self.update_queues()

        self.counter += 1

    def get_free_space(self):
        """Checks if there exists some empty cells for an agent to merge into the main ramp
        Returns all the cells that are free for the agents on the on ramp to merge into"""
        empty_spaces = []
        x = TrafficLight.merge_begin

        while TrafficLight.merge_begin <= x <= TrafficLight.merge_end:
            # while the cell runs parallel to the main road
            if self.model.grid.is_cell_empty((x, 0)) and self.model.grid.is_cell_empty((x + 1, 0)):
                # if the current cell and the next cell are empty append the next cell
                empty_spaces.append(x + 1)
                x += 2
            else:
                x += 1

        return empty_spaces

    def update_queues(self):
        """Update the queues on both sides of the traffic light"""
        # add a certain amount of cars to the on ramp
        self.on_ramp_queue.extend([1 for x in range(self.cars_amount)])
        # update the wait queue by removing the cars that went onto the on ramp
        self.wait_queue = self.wait_queue[self.cars_amount:]

    def merging_cars(self):
        """"""
        empty_spaces = self.get_free_space()

        while len(self.on_ramp_queue) > 0:

            if len(empty_spaces) > 0:
                pass
            else:
                break
