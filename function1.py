import random
import copy

class Individual:
    def __init__(self, N):
        self.gene = [0.0] * N
        self.fitness = 0.0

# Updated fitness function based on the given f(x)
def fitness_function(individual):
    d = len(individual.gene)
    fitness = (individual.gene[0] - 1) ** 2  # First term
    for i in range(1, d):
        fitness += i * ((2 * individual.gene[i] ** 2) - individual.gene[i - 1]) ** 2
    return fitness

def generate_population(size, N, MIN, MAX):
    population = []
    for x in range(size):
        tempgene = []
        for y in range(N):
            tempgene.append(random.uniform(MIN, MAX))
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
        if population[parent1].fitness < population[parent2].fitness:  # Minimize fitness
            new_population.append(population[parent1])
        else:
            new_population.append(population[parent2])
    return new_population

def multi_point_crossover(offspring, N, crossover_prob, num_points):
    for i in range(0, len(offspring), 2):
        if i + 1 < len(offspring) and random.random() < crossover_prob:  # Apply crossover with probability
            points = sorted(random.sample(range(1, N), num_points))  # Choose crossover points
            toff1 = copy.deepcopy(offspring[i])
            toff2 = copy.deepcopy(offspring[i + 1])
            for j, point in enumerate(points):
                if j % 2 == 0:  # Swap segments
                    toff1.gene[point:] = offspring[i + 1].gene[point:]
                    toff2.gene[point:] = offspring[i].gene[point:]
            offspring[i] = toff1
            offspring[i + 1] = toff2

def bitwise_mutation(offspring, N, MUTRATE, MIN, MAX, MUTSTEP):
    for i in range(len(offspring)):
        newind = Individual(N)
        newind.gene = []
        for j in range(N):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            if mutprob < MUTRATE:
                alter = random.uniform(-MUTSTEP, MUTSTEP)
                gene = gene + alter
                if gene > MAX:
                    gene = MAX
                if gene < MIN:
                    gene = MIN
            newind.gene.append(gene)
        offspring[i] = newind

if __name__ == "__main__":
    # Parameters
    N = 20  # Number of dimensions (genes)
    P = 50  # Population size
    T = 2  # Tournament size
    MUTRATE = 1.5  # Mutation rate
    MUTSTEP = 5  # Mutation step size
    MIN = -10.0  # Lower bound for genes
    MAX = 10.0  # Upper bound for genes
    runs = 5  # Number of runs
    crossover_prob = 0.8  # Probability of applying crossover
    num_points = 2  # Number of crossover points
    generations = 50  # Number of generations per run

    all_runs_best_fitness = []
    all_runs_average_fitness = []

    for run in range(runs):
        print(f"Run {run + 1}/{runs}")
        # Generate initial population
        population = generate_population(P, N, MIN, MAX)

        generation_best_fitness = []
        generation_average_fitness = []

        for generation in range(generations):
            # Perform tournament selection
            offspring = tournament_selection(population, T)
            # Apply multi-point crossover
            multi_point_crossover(offspring, N, crossover_prob, num_points)
            # Apply mutation
            bitwise_mutation(offspring, N, MUTRATE, MIN, MAX, MUTSTEP)
            # Update fitness values for offspring
            for individual in offspring:
                individual.fitness = fitness_function(individual)
            # Replace old population with offspring
            population = copy.deepcopy(offspring)

            # Calculate statistics
            generation_fitness_values = [individual.fitness for individual in population]
            best_fitness = min(generation_fitness_values)  # Minimize fitness
            average_fitness = sum(generation_fitness_values) / len(generation_fitness_values)

            generation_best_fitness.append(best_fitness)
            generation_average_fitness.append(average_fitness)

            print(f"Generation {generation + 1}: Best Fitness: {best_fitness}, Average Fitness: {average_fitness}")

        # Track run-level statistics
        all_runs_best_fitness.append(min(generation_best_fitness))
        all_runs_average_fitness.append(sum(generation_average_fitness) / generations)

        print("-" * 50)

    # Calculate overall averages across runs
    overall_average_best_fitness = sum(all_runs_best_fitness) / runs
    overall_average_average_fitness = sum(all_runs_average_fitness) / runs

    print("Summary:")
    print(f"Last Run Average Fitness: {all_runs_average_fitness[-1]}")
    print(f"Average Best Fitness Across All Runs: {overall_average_best_fitness}")
    print(f"Average Fitness Across All Runs: {overall_average_average_fitness}")
