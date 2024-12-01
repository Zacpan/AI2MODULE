import random
import copy

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


def single_point_crossover(offspring, N):
    for i in range(0, len(offspring), 2):
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i + 1])
        temp = copy.deepcopy(offspring[i])
        crosspoint = random.randint(1, N)
        for j in range(crosspoint, N):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        offspring[i] = copy.deepcopy(toff1)
        offspring[i + 1] = copy.deepcopy(toff2)


def bitwise_mutation(offspring, N, MUTRATE):
    for i in range(len(offspring)):
        newind = Individual(N)
        newind.gene = []
        for j in range(N):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            if mutprob < MUTRATE:
                gene = 1 if gene == 0 else 0
            newind.gene.append(gene)
        offspring[i] = newind


#Test function from worksheet 1
def test_function(ind):
    utility = 0
    for i in range(N):
        utility = utility + ind.gene[i]
    return utility


if __name__ == "__main__":
    N = 50
    P = 50
    T = 2
    MUTRATE = 0.01
    generations = 50

    population = generate_population(P, N)

    for _ in range(generations):
        offspring = tournament_selection(population, T)
        single_point_crossover(offspring, N)
        bitwise_mutation(offspring, N, MUTRATE)
        for individual in offspring:
            individual.fitness = fitness_function(individual)
        population = copy.deepcopy(offspring)

    best_fitness = max(ind.fitness for ind in population)
    avg_fitness = sum(ind.fitness for ind in population) / len(population)

    print(f"Best Fitness: {best_fitness}, Average Fitness: {avg_fitness}")
