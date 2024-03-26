import numpy as np
import time

def generate_initial_population(population_size, num_objects):
    return np.random.randint(2, size=(population_size, num_objects))

def is_valid(solution, weights, max_weight):
    total_weight = np.sum(solution * weights)
    return total_weight <= max_weight

def evaluate_population(population, values):
    return np.sum(population * values, axis=1)

def parse_rucksack_data(file_path):
    values = []
    weights = []
    max_weight = None
    num_objects = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_objects = int(lines[0])
        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 3:
                values.append(int(parts[1]))
                weights.append(int(parts[2]))
            elif len(parts) == 1:
                max_weight = int(parts[0])

    return num_objects, values, weights, max_weight

def tournament_selection(population, scores, tournament_size):
    selected_indices = np.random.choice(len(population), size=tournament_size, replace=False)
    tournament_scores = scores[selected_indices]
    return population[selected_indices[np.argmax(tournament_scores)]]

def crossover(parent1, parent2):
    crossover_point = np.random.randint(1, len(parent1))
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

def mutate(solution, mutation_rate):
    mutation_indices = np.random.rand(len(solution)) < mutation_rate
    solution[mutation_indices] = 1 - solution[mutation_indices]
    return solution

def genetic_algorithm(num_objects, values, weights, max_weight, population_size, generations, tournament_size, mutation_rate):
    for _ in range(10):
        population = generate_initial_population(population_size, num_objects)
        best_solution = None
        best_score = float('-inf')
        valid_scores = []
        start_time = time.time()

        for _ in range(generations):
            scores = evaluate_population(population, values)
            valid_indices = [i for i in range(len(population)) if is_valid(population[i], weights, max_weight)]
            valid_scores.extend(scores[valid_indices])

            if valid_indices:
                best_idx = valid_indices[np.argmax(scores[valid_indices])]
                if scores[best_idx] > best_score:
                    best_solution = population[best_idx]
                    best_score = scores[best_idx]

            next_population = []
            for _ in range(population_size // 2):
                parent1 = tournament_selection(population, scores, tournament_size)
                parent2 = tournament_selection(population, scores, tournament_size)
                child1, child2 = crossover(parent1, parent2)
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)
                next_population.extend([child1, child2])

            population = np.array(next_population)

        end_time = time.time()
        runtime = end_time - start_time
        average_valid_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

        return best_solution, best_score, runtime, average_valid_score


