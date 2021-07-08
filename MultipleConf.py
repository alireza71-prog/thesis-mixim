from Simulation import Simulation
import time
import pickle
from multiprocessing import Pool
from util import Capacity
from util import Weights
from util import OptimizedPositions
from util import PositionErrorRate
import configparser
def main(rate):

    config = configparser.ConfigParser()
    config.read('ConfigFile.ini')
    topology = config['TOPOLOGY']['topology']
    mix_type = config['MIXING']['mix_type']
    routing = 'source'

    bandiwdth_per_mix = 10000
    optimizedbandwidth = True
    #Clients
    n_clients = int(config['DEFAULT']['n_clients'])
    lambda_c =  float(config['DEFAULT']['lambda_c'])
    #For Stratified Topology
    n_layer = 3
    n_mix_per_layer = 6  #int(config['TOPOLOGY']['l_mixes_per_layer'])
    total_Number_Mixes= n_layer * n_mix_per_layer

    mu = 1 #(int(config['TOPOLOGY']['E2E']) - (n_layer + 1)*0.05)/n_layer
    threshold = int(config['MIXING']['threshold'])
    pool_size = float(config['MIXING']['flush_percent'])
    timeout = float(config['MIXING']['timeout'])

    # Threat Model
    corrupt_mixes = 0 # * (n_mix_per_layer*n_layer) # int(config['THREATMODEL']['corrupt_mixes'])
    balanced_corruption = bool(config['THREATMODEL']['balanced_corruption'])
    #balanced_corruption = [16/40, 16/40, 1/40,1/40,1/40,1/40,1/40,1/40,1/40,1/40]
    n_cascade = 2
    #Dummies
    link_dummies = True #config['DUMMIES']['link_based_dummies']
    try:
        rate_dummies =float(config['DUMMIES']['rate_dummies'])
    except:
        rate_dummies =None

    capacity = Capacity(bandiwdth_per_mix,total_Number_Mixes)
    if optimizedbandwidth:
        capacitiesOrganized = OptimizedPositions(capacity, n_layer)
    else:
        error = 0.05
        capacitiesOrganized = PositionErrorRate(error)
    weights = Weights(n_layer, n_mix_per_layer)
    # weight_l1 = [1/3,1/3,1/3]
    # weights.append(weight_l1)
    # weights.append(weight_l1)
    # weights.append(weight_l1)

    simulation = Simulation(mix_type=mix_type, simDuration=50, rate_client=1/lambda_c, mu=mu, logging=True,
                            topology=topology, n_clients=n_clients, flushPercent=pool_size, printing=True, flushtime=timeout, capacity=capacitiesOrganized, bandwidth=threshold, routing=routing, n_layers=n_layer,
                            n_mixes_per_layer=n_mix_per_layer,corrupt= corrupt_mixes,UniformCorruption= balanced_corruption,probabilityMixes=weights,nbr_cascacdes = n_cascade, ClientDummy=None, LinkDummies = link_dummies,RateDummies = None,
                            Network_template=None)

    now = time.time()
    entropy, entropy_mean, entropy_median , entropy_q25, meanEps, delta= simulation.run()
    if simulation.printing:
        print('Simulation runtime: {}'.format(time.time() - now))

    return [entropy, entropy_mean, entropy_median , entropy_q25, meanEps, delta]


if __name__ == "__main__":
    p = Pool(processes=1, maxtasksperchild=1)
    param = [1]
    result = p.map(main,param, chunksize=1)
    table_entropy = []
    table_mean_entropy = []
    table_median_entropy = []
    table_q25_entropy = []
    table_epsilon = []
    table_delta_epsilon = []
    for item in result:
        table_entropy.append(item[0])
        table_mean_entropy.append(item[1])
        table_median_entropy.append(item[2])
        table_q25_entropy.append(item[3])
        table_epsilon.append(item[4])
        table_delta_epsilon.append(item[5])
    print("Entropy", table_entropy)
    print("Mean Entropy", table_mean_entropy)
    print("Mediane Entropy", table_median_entropy)
    print("Quanile Entropy 0.25", table_q25_entropy)
    print("Mean Epsilon", table_epsilon)
    print("Delta Epsilon", table_delta_epsilon)









