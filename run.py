from route_66.model import RoadModel

model = RoadModel(6, 60)
for _ in range(100):
    model.step()

    