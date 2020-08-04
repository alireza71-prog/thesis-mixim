import simpy
from Client import Client
from Network import Network
from Simulation import Simulation
import pandas as pd

def main():
    # mix_type : poisson, time, pool
    # routing : hopbyhop , sourcenm
    topology = 'stratified'
    mix_type = 'poisson'
    routing = 'source'
    simulation = Simulation(mix_type=mix_type, routing=routing, n_clients=100, n_msgs=100, rate_client=1/100)
    simulation.run()


if __name__ == "__main__":
    main()
