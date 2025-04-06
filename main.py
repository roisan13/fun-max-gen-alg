import math
import random
import sys

file = open("evolution.txt", "w")
sys.stdout = file


no_individuals = 20
domain_left = -1
domain_right = 2

param1 = -1
param2 = 1
param3 = 2

precision = 6
crossover_prob = 0.25
mutation_prob = 0.01
no_generations = 50

chrom_length = math.ceil(math.log2((domain_right - domain_left) * (10 ** precision)))

def fitness(x):
    return param1 * (x ** 2) + param2 * x + param3

def encode(x):
    max_val = 2 ** chrom_length - 1
    val = round((x - domain_left) * max_val / (domain_right - domain_left))
    return format(val, f'0{chrom_length}b')

def decode(x):
    x_int = int(x, 2)
    max_val = 2 ** chrom_length - 1
    return round(domain_left + (domain_right - domain_left) * x_int / max_val, precision)

def print_population(pop):
    # Output
    for i in range(no_individuals):
        print(f"{i + 1:<5}: {encode(pop[i]):<22} x = {pop[i]:<10.5f} f = {fitness(pop[i]):<15f}")


def init_population():
    return [round(random.random() * (domain_right - domain_left) + domain_left, precision)
            for _ in range(no_individuals)]


def binary_search(cumulative_probs, u):
    left = 0
    right = len(cumulative_probs) - 1

    while left < right:
        mid = (left + right) // 2
        if cumulative_probs[mid] <= u < cumulative_probs[mid + 1]:
            return mid
        elif u < cumulative_probs[mid]:
            right = mid
        else:
            left = mid + 1
    return left - 1


def roulette_selection(population, firstIteration):
    fitness_values = [fitness(ind) for ind in population]
    fitness_sum = sum(fitness_values)
    probabilities = [f_value / fitness_sum for f_value in fitness_values]

    # Output
    if firstIteration:
        print("\nProbabilitati selectate")
        for i in range (no_individuals):
            print(f"cromozom {i + 1} probabilitate {probabilities[i]}")

    cumulative_probs = [0]
    for p in probabilities:
        cumulative_probs.append(cumulative_probs[-1] + p)

    # Output
    if firstIteration:
        print("\nIntervale probabilitati selectate")
        for p in cumulative_probs:
            print(p, end=' ')
        print()

    selected = []
    for _ in range(no_individuals):
        u = random.random()
        index = binary_search(cumulative_probs, u)

        # Output
        if (firstIteration):
            print(f"u = {u:<2f} selectam cromozomul {index + 1}")
        selected.append(population[index])

    return selected

def one_point_crossover(parent1, parent2, firstIteration):
    length = len(parent1)
    point = random.randint(0, length - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    if firstIteration:
        print(f"{parent1} {parent2} punct {point} \nRezultat {child1} {child2}")

    return child1, child2

def crossover_population(pop, firstIteration):
    # Output
    if firstIteration:
        print(f"\nProbabilitatea de incrucisare: {crossover_prob}")

    selected_for_crossover = []
    for i in range(len(pop)):
        u = random.random()

        if (u < crossover_prob):
            selected_for_crossover.append(i)
            if (firstIteration):
                print(f"{i}: {encode(pop[i])} u={u}<{crossover_prob} participa")
        else:
            if (firstIteration):
                print(f"{i}: {encode(pop[i])} u={u}")

    for i in range(0, len(selected_for_crossover) - 1, 2):
        parent1, parent2 = encode(pop[selected_for_crossover[i]]), encode(pop[selected_for_crossover[i + 1]])

        if firstIteration:
            print(f"Recombinare dintre cromozomul {selected_for_crossover[i]} cu cromozomul {selected_for_crossover[i + 1]}:")
        child1, child2 = one_point_crossover(parent1, parent2, firstIteration)

        pop[i] = decode(child1)
        pop[i+1] = decode(child2)


def mutate_population(pop, firstIteration):

    if firstIteration:
        print(f"Probabilitate de mutatie pentru fiecare gena: {mutation_prob}\nAu fost modificati cromozomii: ")


    for idx, individual in enumerate(pop):
        mutated_chrom = list(encode(individual))
        modified = False

        for gene_idx, bit in enumerate(mutated_chrom):
            if random.random() < mutation_prob:
                mutated_chrom[gene_idx] = '1' if bit == '0' else '0'
                modified = True

        if firstIteration and modified:
            print(idx + 1)

        pop[idx] = decode(''.join(mutated_chrom))


def elitist_selection(population, intermediary_pop):
    max_fitness_individual = max(population, key=fitness)
    intermediary_pop[0] = max_fitness_individual
    return intermediary_pop[1:]


population = init_population()
# Output
print("Populatia initiala")
print_population(population)

# print(decode(encode(-0.9999)))

for gen in range(no_generations):
    isFirstIter = (gen == 0)

    # print_population(population)

    elite_individual = max(population, key=fitness)

    intermediary_pop = roulette_selection(population, isFirstIter)

    if isFirstIter:
        print("Dupa selectie:")
        print_population(intermediary_pop)

    crossover_population(intermediary_pop, isFirstIter)

    if isFirstIter:
        print("Dupa recombinare:")
        print_population(intermediary_pop)

    mutate_population(intermediary_pop, isFirstIter)

    if isFirstIter:
        print("Dupa mutatie:")
        print_population(intermediary_pop)

    max_fitness = max(fitness(ind) for ind in intermediary_pop)
    mean_fitness = sum(fitness(ind) for ind in intermediary_pop) / len(intermediary_pop)

    if gen == 1:
        print("Evolutia max si mean fitness")
    if gen > 1:
        print(f"Max fitness: {max_fitness:<10.10f}\t\tMean fitness: {mean_fitness}")

    intermediary_pop[0] = elite_individual
    population = intermediary_pop


file.close()
sys.stdout = sys.__stdout__