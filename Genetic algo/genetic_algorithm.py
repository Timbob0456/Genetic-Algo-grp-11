import numpy as np
import random as rand
#Encoding: Permutation encoding, where each individual in the population represents a possible route through the cities.
POPULATION_SIZE = 8
GENERATIONS = 10
cities = ['A', 'B', 'C', 'D']

"""
Dictionary chosen because of string keys for cities and easy access to distances between cities. 
The values are nested dictionaries where the keys are the destination cities and the values are the distances from the 
source city to the destination city. 
This structure allows for efficient lookups of distances between any two cities in the traveling salesman problem.
"""
distances = {
     'A': {'A': 0, 'B': 5, 'C': 10, 'D': 15},
    'B': {'A': 5, 'B': 0, 'C': 20, 'D': 25},
    'C': {'A': 15, 'B': 27, 'C': 0, 'D': 30},
    'D': {'A': 20, 'B': 27, 'C': 30, 'D': 0}
    
}

# Population initialization function: Generate a random route for the traveling salesman problem
def initialize_population(population_size, cities):
    population = []
    for _ in range(population_size):
        route = generate_random_route(cities)
        population.append(route)
    return population

#Fisher-Yates shuffle algorithm to create a random route by shuffling the order of cities
def fy_shuffle(cities):
    for i in range(len(cities)):
        j = rand.randrange(i,len(cities))
        temp = cities[i]
        cities[i] = cities[j]
        cities[j] = temp

def generate_random_route(cities):
    route = cities.copy() #Create a copy of the cities list to avoid modifying the original
    fy_shuffle(route) #Create a random route by shuffling the order of cities by implementing a function
    return route

#Fitness function: Calculate the total distance of the route (lower is better)
def compute_total_distance(route, distances):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i]][route[i+1]] #Calculate the distance between consecutive cities in the route
    total_distance += distances[route[-1]][route[0]] #Return to the starting city to complete the tour outside of the loop
    return total_distance

population = initialize_population(POPULATION_SIZE, cities)
for route in population:
    fitness = compute_total_distance(route, distances)
    print(f"Route: {route}, Total Distance: {fitness}")

#Selection - Select individuals based on their fitness to create offspring for the next generation (e.g., tournament selection, roulette wheel selection, etc.)
def tournament_selection(population, fitness, k=2):
    selected = []
    for _ in range(len(population)):
        idxs = rand.sample(range(len(population)), k) #Randomly select k individuals from the population
        
        best_idx = idxs[0]
        for i in idxs:
            if fitness[i] < fitness[best_idx]: #Select the individual with the lowest total distance (best fitness)
                best_idx = i
        selected.append(population[best_idx])
    return selected
#Crossover - Combine two parent solutions to create offspring (e.g., one-point crossover, two-point crossover, uniform crossover, etc.)
def one_point_crossover(parent1, parent2):
    point = rand.randint(1, len(parent1) - 1) 
    offspring1 = parent1[:point] + [city for city in parent2 if city not in parent1[:point]] 
    offspring2 = parent2[:point] + [city for city in parent1 if city not in parent2[:point]]
    return offspring1, offspring2

def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(rand.sample(range(1, len(parent1) - 1), 2)) 
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:] 
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:] 
    return offspring1, offspring2

def uniform_crossover(parent1, parent2):
    offspring1, offspring2 = [], []
    for i in range(len(parent1)):
        if rand.random() < 0.5:
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        else:
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])
    return offspring1, offspring2
     
#Mutation - Introduce random changes to offspring to maintain genetic diversity (e.g., bit flip mutation, swap mutation, etc.)
def mutation_swap(cities):
    idx1, idx2 = rand.sample(range(len(cities)), 2) 
    cities[idx1], cities[idx2] = cities[idx2], cities[idx1] 
    return cities
     
#New Population - Replace the current population with the new offspring, often using elitism to retain the best solutions from the previous generation
def create_new_population(selected, crossover_rate=0.8, mutation_rate=0.1):
    new_population = []
    for i in range(0, len(selected) - 1 , 2):
        parent1 = selected[i].copy() 
        parent2 = selected[i + 1].copy() 
        
        if rand.random() < crossover_rate: 
            offspring1, offspring2 = one_point_crossover(parent1, parent2)
        else:
            offspring1, offspring2 = parent1.copy(), parent2.copy() 
        
        if rand.random() < mutation_rate: 
            offspring1 = mutation_swap(offspring1)
        if rand.random() < mutation_rate:
            offspring2 = mutation_swap(offspring2)
        
        new_population.extend([offspring1, offspring2]) 
    return new_population
     
#Repeat (Evolution loop) - Repeat the process for a specified number of generations or until a stopping criterion is met (e.g., convergence, maximum fitness, etc.)
