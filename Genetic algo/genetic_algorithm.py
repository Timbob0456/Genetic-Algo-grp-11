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

#Mutation - Introduce random changes to offspring to maintain genetic diversity (e.g., bit flip mutation, swap mutation, etc.)

#New Population - Replace the current population with the new offspring, often using elitism to retain the best solutions from the previous generation

#Repeat (Evolution loop) - Repeat the process for a specified number of generations or until a stopping criterion is met (e.g., convergence, maximum fitness, etc.)
