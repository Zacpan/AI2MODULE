#AI2 Module worksheet 1
#This worksheet is inteded to implement a simple genetic algorithm

import random

class Individual:
    def __init__(self, N):
        self.gene = [0] * N
        self.fitness = 0


def fitness_function(individual):
    return sum(individual.gene)


def generate_population(size, N):
    population = []
    
    for x in range(size):
        tempgene = []
        for y in range(N):
            tempgene.append(random.randint(0, 1))

        newind = Individual(N)
        newind.gene = tempgene.copy()
        newind.fitness = fitness_function(newind)
        

        population.append(newind)
    
    return population


def tournament_selection(population, T):
    new_population = []
    for i in range(len(population)):
        parent1 = random.randint(0, len(population) - 1)
        parent2 = random.randint(0, len(population) - 1)
        if population[parent1].fitness > population[parent2].fitness:
            new_population.append(population[parent1])
        else:
            new_population.append(population[parent2])
    return new_population




#Test function from worksheet 1
def test_function( ind ):
    utility=0
    for i in range(N):
        utility = utility + ind.gene[i]
    return utility
    


if __name__ == "__main__":
    N = 10
    P = 50
    T = 2

    population = generate_population(P, N)

    parents = []
    for i in range(P):
        tempparent = tournament_selection(population, T)
        parents.append(tempparent)


    initial_fitness_values = []
    for individual in population:
        initial_fitness_values.append(individual.fitness)


    highest_fitness = initial_fitness_values[0]
    for fitness in initial_fitness_values:
        if fitness > highest_fitness:
            best_fitness = fitness


    sumof_fitness = 0
    for fitness in initial_fitness_values:
        sumof_fitness += fitness
    average_fitness = sumof_fitness / len(initial_fitness_values)


    print(f"Best Fitness: {highest_fitness}, Average Fitness {average_fitness}")




