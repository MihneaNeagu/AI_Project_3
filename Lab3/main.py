import numpy as np
from evolutive_knapsack import genetic_algorithm, parse_rucksack_data
from evolutive_tsp import parse_input, TSPSolver


def main_genetic_algorithm():
    num_objects, values, weights, max_weight = parse_rucksack_data("data.txt")
    population_size = 30
    generations = 10000
    tournament_size = 10
    mutation_rate = 0.2

    best_solution, best_score, runtime, average_valid_score = genetic_algorithm(num_objects, values, weights,
                                                                                max_weight,
                                                                                population_size, generations,
                                                                                tournament_size,
                                                                                mutation_rate)

    print("Genetic Algorithm Results:")
    print("Best Solution:", best_solution)
    print("Best Score:", best_score)
    print("Average score:", average_valid_score)
    print("Runtime:", runtime, "seconds")


def main_evolutive_tsp():
    input_file = 'tsp.txt'
    population_size = 30
    num_generations = 100000
    crossover_prob = 0.8
    mutation_prob = 0.2
    cities = parse_input(input_file)
    solver = TSPSolver(cities, population_size, num_generations, crossover_prob, mutation_prob)
    best_solution, best_distance, num_solutions, avg_distance, runtime = solver.genetic_tsp()
    print("Number of generations:", num_solutions)
    print("Average route length from all generations:", avg_distance)
    print("Best distance:", best_distance)
    print("Average runtime:", runtime)


if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Evolutive Knapsack Problem")
        print("2. Evolutive TSP Problem")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            main_genetic_algorithm()
            break
        elif choice == "2":
            main_evolutive_tsp()
            break
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

