from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from route_66.model import RoadModel
from route_66.agent import CarAgent

# color spectrum from red to blue
colour_spectrum = ["#ff3333", "#ffb133", "#92ff33", "#33ffc9", "#3366ff"]


def car_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {}
    # update portrayal characteristics for each CarAgent object
    if isinstance(agent, CarAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = .9
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        # change the agents color to its velocity
        portrayal["Color"] = colour_spectrum[agent.velocity - 1]

    return portrayal


model_params = {"N" : UserSettableParameter("slider", "Cars", 1, 1, 59,
                                            description="Number of cars")}

canvas_element = CanvasGrid(car_portrayal, 60, 1)

chart_element = ChartModule([{"Label" : "Average Velocity", "Color" : colour_spectrum[4]}])

server = ModularServer(RoadModel, [canvas_element, chart_element], 
                        "Nagel-Schreckenberg model", 
                        model_params=model_params)