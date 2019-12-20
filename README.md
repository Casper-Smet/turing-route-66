# Turing Route 66

Git repository for the assignment 'Touring Machines' for the course Simulation Tooling for the bachelor programme Artificial Intelligence at the HU University of Applied Sciences Utrecht.

***
To run the simulation in the interactive webserver, the file `run.py` needs to be executed. This will open the webpage `http://127.0.0.1:8521/`

The plots belonging to the simulation and the batch run can be seen in the Jupyter Notebook `Simulation Analysis.ipynb`.

To update the documentation, the command `make html` needs to be run. The documentation can also be viewed on [Read The Docs](https://turing-route-66.readthedocs.io/en/latest/ "readthedocs.io").

Python 3.8.X is currently not supported. It is recommended to run the simulation in Python 3.6.x or 3.7.x.

## Abstract

With world poverty rates declining and access to private transportation methods increasing, road congestion is an ever-growing problem. Using the conducted experiment, we attempted to answer the following question: How does a traffic light on an on ramp and its timing affect throughput on a highway? In order to do this, we implemented and altered the Nagel-Schreckenberg congestion model. 
    
Increasing the timer duration of the traffic light showed a positive effect on the throughput of the main road. Increasing the timer duration also caused the buildup of a large queue on the on ramp. Further research may focus on not only congestion on the highway, but also that of the on ramp. Finding the right balance between the two will hopefully improve throughput for the road network as a whole.
