from route_66.server import server
from route_66.visualisation import plot
from route_66.batch_run import run_batch

# server.launch()
# plot(100, 35, length=100, p=0.3, grid=True)
run_batch(N=[10, 25, 30], timer=[2, 3, 4, 5, 6, 7, 8])
