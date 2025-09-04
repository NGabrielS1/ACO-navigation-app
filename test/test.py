import time
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations

seed = 67
random.seed(seed)
np.random.seed(seed)
data = pd.read_csv("data.csv")

init_p = 0.2
alpha = 1
beta = 2
added_p = 10
evap_rate = 0.1
ants = 100

def get_dist_matrix(cities: int) -> pd.DataFrame:
    city_names = data[data["Num Cities"]==float(cities)]["Start"].to_list()
    city_names = list(sorted(set(city_names)))
    dist_matrix = pd.DataFrame(index=city_names, columns=city_names)

    for city1 in city_names:
        for city2 in city_names:
            dist = 0
            if city1 != city2:
                dist = float(data[(data["Num Cities"]==float(cities)) & (data["Start"]==city1) & (data["End"]==city2)]["Distance"].item().replace(" km", ""))
            dist_matrix.loc[city1, city2] = dist

    return dist_matrix

def ant_colony_optimization(dist_matrix, eta, alpha, beta, p, q, num_ants):
    #create pheromone table
    pheromones = dist_matrix.copy()
    pheromones[pheromones!=0] = eta

    cities = dist_matrix.columns.to_list()
    best_dist = float('inf')

    start_time = time.time()

    #run iterations
    for i in range(num_ants):

        #refresh variables
        tread = []
        dist = 0

        choices = cities.copy()
        current = choices[0]
        choices.remove(current)

        #ant moves and gets route data
        for i in range(len(cities)-1):
            probabilities = [] #get probabilities
            denominator = sum([(pheromones.loc[current, choice2]**alpha) / (dist_matrix.loc[current, choice2]**beta) for choice2 in choices])
            for choice in choices:
                numerator = (pheromones.loc[current, choice]**alpha) / (dist_matrix.loc[current, choice]**beta)
                probabilities.append(numerator/denominator)
            
            next = np.random.choice(a=choices, p=probabilities) #list next destination and move on
            tread.append([current,next])
            dist += dist_matrix.loc[current, next]
            current = next
            choices.remove(current)
        dist += dist_matrix.loc[current, cities[0]]

        #update pheromones
        pheromones[pheromones!=0] *= (1-p) #evaporate
        for route in tread:
            pheromones.loc[route[0], route[1]] += (q/dist)
            pheromones.loc[route[1], route[0]] += (q/dist)
        
        if dist < best_dist: best_dist = dist
    
    end_time = time.time()
    
    return best_dist, (end_time-start_time)

def brute_force(dist_matrix):
    cities = dist_matrix.columns.to_list()
    best_dist = float('inf')

    choices = cities.copy()
    start = choices[0]
    choices.remove(start)

    start_time = time.time()
    for route in permutations(choices):
        dist = 0
        temp = [start] + list(route) + [start]
        for i in range(len(cities)):
            dist += dist_matrix.loc[temp[i], temp[i+1]]
        if dist < best_dist: best_dist = dist
    end_time = time.time()
    
    return best_dist, (end_time-start_time)

def test():
    aco_dist = []
    aco_time = []
    bf_dist = []
    bf_time = []

    for i in range(48-3):
        print(f"Cities: {i+3}")
        dist_matrix = get_dist_matrix(i+3)
        a_dist, a_time = ant_colony_optimization(dist_matrix, init_p, alpha, beta, evap_rate, added_p, ants)
        b_dist, b_time = brute_force(dist_matrix)
        aco_dist.append(a_dist)
        aco_time.append(a_time)
        bf_dist.append(b_dist)
        bf_time.append(b_time)
    print("Done!")
    
    list_o_numbers = [3+i for i in range(48-3)]
    
    plt.figure()
    plt.plot(list_o_numbers, aco_dist, label="ACO")
    plt.plot(list_o_numbers, bf_dist, label="Brute Force")
    plt.xlabel('Cities')
    plt.ylabel('Distance (km)')
    plt.title("Best Distance")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(list_o_numbers, aco_time, label="ACO")
    plt.plot(list_o_numbers, bf_time, label="Brute Force")
    plt.xlabel('Cities')
    plt.ylabel('Time (s)')
    plt.title("Time per n Cities")
    plt.legend()
    plt.grid(True)
    plt.show()

test()