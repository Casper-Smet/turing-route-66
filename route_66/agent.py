from mesa import Agent


class CarAgent(Agent):
    """
    An agent with a velocity of 1-5 and a position. Random initial velocity
    """
    init_velocity = 5
    max_velocity = 5
    p = 0.5

    def __init__(self, unique_id, model, tf):
        super().__init__(unique_id, model)
        self.velocity = CarAgent.init_velocity
        self.is_from_traffic_light = tf

    def acceleration(self):
        """
        Increases velocity by one unit if it is smaller than CarAgent.max_velocity

        :return: The current velocity of the agent
        """
        if self.velocity < CarAgent.max_velocity:
            self.velocity += 1

        return self.velocity

    def braking(self):
        """
        If the distance between an agent and the agent in front of it is smaller than the velocity
        the velocity is reduced to the number of emtpy cells in front of the car

        :return: The current velocity of the agent
        """
        x, y = self.pos
        for i in range(1, self.velocity + 1):
            x0, y0 = self.model.grid.torus_adj((x + i, y))

            if not self.model.grid.is_cell_empty((x0, y0)):
                self.velocity = i - 1
                break

        return self.velocity

    def randomisation(self):
        """
        If an agent's velocity is greater than 1,
        it may slow down by one unit of velocity randomly with a probability of CarAgent.p

        :return: The current velocity of the agent
        """
        if self.velocity > 1:
            if self.random.random() < CarAgent.p:
                self.velocity -= 1

        return self.velocity

    def move(self):
        """
        The agent is moved forward the number of cells equal to their velocity
        """
        x, y = self.pos
        new_pos = (x + self.velocity, y)
        new_pos = self.model.grid.torus_adj(new_pos)

        self.model.grid.move_agent(self, new_pos)

    def delete(self):
        """
        Deletes the merged agents from the on ramp that have reached the end of the main road
        """
        if self.is_from_traffic_light:
            # the agent is from the on ramp
            x, y = self.pos
            if 0 <= x <= 5:
                self.model.delete_agent(self)


class TrafficLight(object):
    """
    A traffic light that holds a list with waiting cars and cars that want to merge to the main road
    """
    cars_amount = 1

    def __init__(self, unique_id, model, timer, ramp_begin, ramp_len):
        self.unique_id = unique_id
        self.model = model
        self.current_car_id = 0

        self.wait_queue = 1
        self.on_ramp_queue = 0

        self.timer = timer
        self.counter = 0

        self.on_ramp_begin = ramp_begin
        self.on_ramp_end = ramp_begin + ramp_len

    def step(self):
        """The update function for the traffic light"""
        if self.counter == self.timer:
            # let cars through
            self.counter = 0
            # update the queues
            self.update_queues()
            # merge the cars
            self.merging_cars()
        else:
            # update the counter
            self.counter += 1

        # add a certain amount of agents to the waiting queue
        self.wait_queue += self.new_agents_to_queue()

    def get_free_space(self):
        """
        Checks if there exists some empty cells for an agent to merge into the main ramp
        Returns all the cells that are free for the agents on the on ramp to merge into
        """
        empty_spaces = []
        x = self.on_ramp_begin

        while self.on_ramp_begin <= x <= self.on_ramp_end:
            # while the cell runs parallel to the main road
            if self.model.grid.is_cell_empty((x, 0)) and self.model.grid.is_cell_empty((x + 1, 0)):
                # if the current cell and the next cell are empty append the next cell
                empty_spaces.append(x + 1)
                x += 2
            else:
                x += 1

        return empty_spaces

    def update_queues(self):
        """
        Update the queues on both sides of the traffic light
        """
        # add a certain amount of agents to the on ramp
        self.on_ramp_queue += TrafficLight.cars_amount
        # update the wait queue by removing the agents that went onto the on ramp
        self.wait_queue -= TrafficLight.cars_amount

    def merging_cars(self):
        """
        Checks if there are agents on the on ramp and if there is room to merge to the main road
        Adds the agents to the main road and updates the on ramp queue
        """
        empty_spaces = self.get_free_space()

        while self.on_ramp_queue > 0:
            # There exist some agents on the on ramp to merge
            if len(empty_spaces) > 0:
                # there is room for merging

                # get the x-coordinate for the merge
                x_corr = empty_spaces.pop()
                # get the label for the agent
                new_label = f"tf_{self.current_car_id}"
                self.current_car_id += 1

                # add the new agent to the model
                self.model.add_agent(new_label, x_corr)
                # update the on_ramp_queue
                self.on_ramp_queue -= 1
            else:
                # no room for merging
                break

    @staticmethod
    def new_agents_to_queue():
        """
        A function to generate an amount of agents per step to wait before the light

        :return: The amount of new cars that are added to the queue
        """
        new_cars = 2
        return new_cars
