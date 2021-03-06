from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from route_66.agent import CarAgent
from route_66.model import RoadModel

# color spectrum from red to blue
colour_spectrum = ["#ff3333", "#ffb133", "#92ff33", "#33ffc9", "#3366ff"]


def car_portrayal(agent):
    """Visualises the cars for the Mesa webserver

    :return: Dictionary containing the settings of an agent"""
    if agent is None:
        return

    portrayal = {}
    # update portrayal characteristics for each CarAgent object
    if isinstance(agent, CarAgent):
        if agent.is_from_traffic_light:
            portrayal["Shape"] = "rect"
            portrayal["w"], portrayal["h"] = .7, .7
        else:
            portrayal["Shape"] = "circle"
            portrayal["r"] = .9
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        # change the agents color to its velocity
        portrayal["Color"] = colour_spectrum[agent.velocity - 1]

    return portrayal


model_params = {"N": UserSettableParameter("slider", "Number of cars", 1, 1, 99, description="Number of cars"),
                "timer": UserSettableParameter("slider", "Timing of the traffic light", 1, 1, 100, description="Timing of the traffic light")}

canvas_element = CanvasGrid(car_portrayal, 100, 1, 800, 10)

chart_velocity = ChartModule([{"Label": "Average Velocity", "Color": colour_spectrum[4]}])

chart_on_ramp_queue = ChartModule([{"Label": "On Ramp Queue", "Color": colour_spectrum[2]}])

chart_N_cars = ChartModule([{"Label": "Amount of cars", "Color": colour_spectrum[0]}])

server = ModularServer(RoadModel, [canvas_element, chart_velocity, chart_N_cars, chart_on_ramp_queue], "Nagel-Schreckenberg model", model_params=model_params)
