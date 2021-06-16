from Simulation import Simulation
import time
from util import Capacity
from util import OptimizedPositions


def main():
    # mix_type : poisson, time, pool
    # routing : hopbyhop , source
    # topology freeroute, stratified, cascade
    topology = 'stratified'
    mix_type = 'poisson'
    routing = 'source'
    arrayofcapacity = []
    # Attention :You must generate an exact number of mixes that n layers* n mixes per layer other wise eroor in probability distribution
    # The function Capacity takes two arguments : First the capacity of the mix, Second The number of mixes of that capacity

    capacity = Capacity(arrayofcapacity, 10000, 3)
    capacitiesOrganized =OptimizedPositions(capacity,3 )

    simulation = Simulation(mix_type=mix_type, simDuration=25, rate_client=1, rateP=1, logging=True, attack=False,
                            topology=topology, n_clients=100, flushPercent=0.7, printing=True, flushtime=4,
                            onemix=False, capacity=capacitiesOrganized, bandwidth=50, routing=routing, n_layers=3, n_mixes_per_layer=3, mixDummyRate=None,
                            Network_template=None)
    now = time.time()
    ent = simulation.run()
    print('Simulation runtime: {}'.format(time.time() - now))
    return ent


if __name__ == "__main__":
    main()
