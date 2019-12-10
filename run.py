from route_66.server import server
from route_66.visualisation import plot
from route_66.batch_run import plot_batch

# server.launch()
# plot(100, 35, length=100, p=0.3, grid=True)
plot_batch(N=[10, 35, 70], timer=[0, 2, 6])
