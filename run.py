from route_66.model import RoadModel
from route_66.server import server
import matplotlib.pyplot as plt

model = RoadModel(6, 60)
for _ in range(100):
    model.step()

if 0:  # Change to 1 for plot
    velocities = model.datacollector.get_agent_vars_dataframe()

    agent0 = velocities.reset_index()
    agent0 = agent0[agent0["AgentID"] == 0]
    agent0.set_index("Step", inplace=True)
    
    print(agent0.head())
    agent0[["Velocity"]].plot()
    plt.show()

server.launch()
