import random as rand
#Encoding: Permutation encoding, where each individual in the population represents a possible route through the cities.
POPULATION_SIZE = 8
GENERATIONS = 10
TOURNAMENT_SIZE = 2
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
ELITE_COUNT = 1
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
        j = rand.randrange(i, len(cities))
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

#Evaluate the fitness of every individual in the population
def evaluate_population(population, distances):
    fitness = []
    for route in population:
        total_distance = compute_total_distance(route, distances)
        fitness.append(total_distance)
    return fitness

#Find the best route in the current population
def get_best_route(population, fitness):
    best_idx = 0
    for i in range(1, len(population)):
        if fitness[i] < fitness[best_idx]:
            best_idx = i
    return population[best_idx].copy(), fitness[best_idx]

#Selection - Select individuals based on their fitness to create offspring for the next generation (e.g., tournament selection, roulette wheel selection, etc.)
def tournament_selection(population, fitness, k=2):
    selected = []
    for _ in range(len(population)):
        idxs = rand.sample(range(len(population)), k) #Randomly select k individuals from the population
        
        best_idx = idxs[0]
        for i in idxs:
            if fitness[i] < fitness[best_idx]: #Select the individual with the lowest total distance (best fitness)
                best_idx = i
        selected.append(population[best_idx].copy())
    return selected

#Crossover - Combine two parent solutions to create offspring while still keeping valid routes
#A single crossover is used here because it preserves permutation encoding more naturally for TSP
def one_point_crossover(parent1, parent2):
    point = rand.randint(1, len(parent1) - 1)
    offspring1 = parent1[:point] + [city for city in parent2 if city not in parent1[:point]]
    offspring2 = parent2[:point] + [city for city in parent1 if city not in parent2[:point]]
    return offspring1, offspring2
     
#Mutation - Introduce random changes to offspring to maintain genetic diversity (e.g., bit flip mutation, swap mutation, etc.)
def mutation_swap(cities):
    idx1, idx2 = rand.sample(range(len(cities)), 2)
    cities[idx1], cities[idx2] = cities[idx2], cities[idx1]
    return cities
     
#New Population - Replace the current population with the new offspring, using elitism to retain the best solutions from the previous generation
def create_new_population(population, fitness, crossover_rate=0.8, mutation_rate=0.1, elite_count=1):
    ranked_population = []
    for i in range(len(population)):
        ranked_population.append((population[i].copy(), fitness[i]))
    ranked_population.sort(key=lambda pair: pair[1])

    new_population = []
    for i in range(elite_count):
        new_population.append(ranked_population[i][0].copy()) #Keep the best route(s) from the previous generation

    selected = tournament_selection(population, fitness, TOURNAMENT_SIZE)

    i = 0
    while len(new_population) < len(population):
        parent1 = selected[i % len(selected)].copy()
        parent2 = selected[(i + 1) % len(selected)].copy()
        i += 2
        
        if rand.random() < crossover_rate:
            offspring1, offspring2 = one_point_crossover(parent1, parent2)
        else:
            offspring1, offspring2 = parent1.copy(), parent2.copy()
        
        if rand.random() < mutation_rate:
            offspring1 = mutation_swap(offspring1)
        if rand.random() < mutation_rate:
            offspring2 = mutation_swap(offspring2)
        
        new_population.append(offspring1)
        if len(new_population) < len(population):
            new_population.append(offspring2)
    return new_population

#Run the genetic algorithm across multiple generations and track improvement
def run_genetic_algorithm():
    population = initialize_population(POPULATION_SIZE, cities)
    fitness = evaluate_population(population, distances)

    print('Initial Population:')
    for route in population:
        total_distance = compute_total_distance(route, distances)
        print(f'Route: {route}, Total Distance: {total_distance}')

    initial_best_route, initial_best_distance = get_best_route(population, fitness)
    print(f'\nInitial Best Route: {initial_best_route}, Total Distance: {initial_best_distance}')

    for generation in range(1, GENERATIONS + 1):
        population = create_new_population(population, fitness, CROSSOVER_RATE, MUTATION_RATE, ELITE_COUNT)
        fitness = evaluate_population(population, distances)
        best_route, best_distance = get_best_route(population, fitness)
        print(f'Generation {generation}: Best Route: {best_route}, Total Distance: {best_distance}')

    final_best_route, final_best_distance = get_best_route(population, fitness)
    print(f'\nFinal Best Route: {final_best_route}, Total Distance: {final_best_distance}')

run_genetic_algorithm()
