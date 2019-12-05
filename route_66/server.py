from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from route_66.model import RoadModel
from route_66.agent import CarAgent

# Blue
blue = "#3349FF"

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
        portrayal["Color"] = blue

    return portrayal

model_params = {"N" : UserSettableParameter("slider", "Cars", 1, 1, 100,
                                            description="Number of cars")}

canvas_element = CanvasGrid(car_portrayal, 60, 1)

server = ModularServer(RoadModel, [canvas_element], 
                        "Nagel-Schreckenberg model", 
                        model_params=model_params)