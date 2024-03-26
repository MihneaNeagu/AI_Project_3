import random
import math
import time


class TSPSolver:
    def __init__(self, cities, population_size, num_generations, crossover_prob, mutation_prob):
        self.cities = cities
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

    def generate_initial_population(self):
        return [random.sample(self.cities, len(self.cities)) for _ in range(self.population_size)]

    def evaluate_fitness(self, solution):
        total_distance = sum(
            self.calculate_distance(solution[i], solution[(i + 1) % len(solution)]) for i in range(len(solution)))
        return total_distance

    def crossover(self, parent1, parent2):
        # 2-opt crossover
        n = len(parent1)
        start = random.randint(0, n - 1)
        end = random.randint(start + 1, n)

        child = [None] * n
        child[start:end] = parent1[start:end]

        remaining = [city for city in parent2 if city not in child]
        idx = end
        for city in remaining:
            if None in child:
                while child[idx % n] is not None:
                    idx += 1
                child[idx % n] = city
                idx += 1
            else:
                break

        return child

    def mutate(self, solution):
        # Swap mutation
        index1, index2 = random.sample(range(len(solution)), 2)
        solution[index1], solution[index2] = solution[index2], solution[index1]
        return solution

    def select_parents(self, population):
        # Tournament selection
        parents = random.sample(population, 2)
        return parents

    def genetic_tsp(self):
        for _ in range(10):
            start_time = time.time()
            population = self.generate_initial_population()
            total_distance = 0
            num_solutions = 0
            best_distance = float('inf')
            best_solution = None

            for _ in range(self.num_generations):
                offspring = []
                for _ in range(len(population)):
                    parent1, parent2 = self.select_parents(population)
                    if random.random() < self.crossover_prob:
                        child = self.crossover(parent1, parent2)
                    else:
                        child = parent1[:]
                    if random.random() < self.mutation_prob:
                        child = self.mutate(child)
                    offspring.append(child)
                population = sorted(offspring, key=self.evaluate_fitness)[:self.population_size]

                # Update statistics
                total_distance += self.evaluate_fitness(population[0])
                num_solutions += 1
                if self.evaluate_fitness(population[0]) < best_distance:
                    best_distance = self.evaluate_fitness(population[0])
                    best_solution = population[0]

            end_time = time.time()
            runtime = end_time - start_time
            return best_solution, best_distance, num_solutions, total_distance / num_solutions, runtime

    def calculate_distance(self, city1, city2):
        xd = city1.x - city2.x
        yd = city1.y - city2.y
        return round(math.sqrt(xd ** 2 + yd ** 2))


class City:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


def parse_input(filename):
    cities = []
    with open(filename, 'r') as file:
        lines = file.readlines()[6:-1]
        for line in lines:
            parts = line.split()
            city = City(int(parts[0]), int(parts[1]), int(parts[2]))
            cities.append(city)
    return cities


def main_evolutive_tsp():
    input_file = 'tsp.txt'
    population_size = 30
    num_generations = 1000
    crossover_prob = 0.8
    mutation_prob = 0.2
    cities = parse_input(input_file)
    solver = TSPSolver(cities, population_size, num_generations, crossover_prob, mutation_prob)
    best_solution, best_distance, num_solutions, avg_distance, runtime = solver.genetic_tsp()
    print("Number of generations:", num_solutions)
    print("Average route length from all generations:", avg_distance)
    print("Best distance:", best_distance)
    print("Average runtime:", runtime)



