from util import *
import random
import csv


# VARIABLE CONSTANTS?
POPULATION_SIZES = [20, 50, 100, 200, 300, 400, 500, 1000]
TOURNAMENT_SIZES = [5, 10, 30, 50, 100, 200, 300, 400, 500]
MUTATION_RATES = [1, 2, 3, 4, 5, 10, 15, 20, 30, 50] #expressed as a percentage
NUM_TRIALS = 10.0

# Weights and values are stored with corresponding indexes i.e. bag 50 has has weight weights[50] and value values[50]
values = []
weights = []

# Reading bank details in
with open("Bank Problem File.txt", 'r') as f:

    # Read in weight limit from first line
    first_line = f.readline()
    weight_limit = get_weight_limit(first_line)

    line_num = 0
    weight_flag = 1
    value_flag = 0

    for line in f:
        # Every 3rd line skip (since it's just "bag i:"), else append onto relevant list based on flag
        if line_num % 3 == 0:
            line_num += 1
            continue
        else:
            # Append the str value converted to a string and cleaned 
            if weight_flag:
                weights.append(float(line.split(':')[1].strip(" ")[:3]))
                weight_flag = 0
                value_flag = 1
            elif value_flag:
                values.append(int(line.split(':')[1].strip(" ")[:3]))
                weight_flag = 1
                value_flag = 0
        line_num += 1

num_bags = len(weights)

# Each combination of pop_size, tourney_size, and mut_rate are ran NUM_TRAILS times so an average can be taken for robust results
with open("results.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile, dialect="excel")
    writer.writerow(["Pop_Size", "Tourney_Size", "Mut_Rate", "Min_Fitness_avg", "Max_Fitness_avg", "Avg_Fitness_avg", "Max_Value_Found_Across_Trials"])

    for POPULATION_SIZE in POPULATION_SIZES:
        for TOURNAMENT_SIZE in TOURNAMENT_SIZES:
            # Tourney size cannot be larger than the population so not every combination of params can be run, only htose that can be are actually run
            if TOURNAMENT_SIZE >= POPULATION_SIZE:
                continue
            else:
                for MUTATION_RATE in MUTATION_RATES:
                    print(f"P:{POPULATION_SIZE} - T:{TOURNAMENT_SIZE} - M:{MUTATION_RATE}")

                    Avg_Fitness_avg, Max_Fitness_avg, Min_Fitness_avg, Max_Value_Found = 0, 0, 0, 0

                    for j in range(int(NUM_TRIALS)):
                        print(f"Trial Number: {j}")
                        # Generate an initial population and evaluate all their fitnesses
                        # Each solution is stored as a list the same length as the number of bags, and a 1 in index i means bag i is in the solution. A 0 means it is not in the solution
                        # The index of the fitness score indicates which solution win populaiton it references i.e. fitnesses[i] is the fitness of population[i]
                        population = []
                        fitnesses = []

                        population = init_pop(weights=weights, pop_size=POPULATION_SIZE)
                        
                        for i in range(POPULATION_SIZE):
                            fitnesses.append(eval_fitness(chromosone=population[i], weights=weights, values=values, limit=weight_limit))

                        #==============Main Algorithm body===============#
                        # 5000 trials means 10000 fitness evaluations as 2 are done per trial
                        for i in range(5000):

                            # Select parent through tournament select
                            parent_a = population[tournament_select(fitnesses=fitnesses, tourney_size=TOURNAMENT_SIZE)]
                            parent_b = population[tournament_select(fitnesses=fitnesses, tourney_size=TOURNAMENT_SIZE)]

                            # Randomly select crossover point in range 0-number of bags and perform crossover on the two parents to get c and d
                            crossover_point = random.randint(0, num_bags)
                            child_c, child_d = crossover(parent1=parent_a, parent2=parent_b, co=crossover_point)
                            
                            # Mutate each gene of c and d, depending on mutation rate, and call them e and f
                            mut_child_e = mutate(chromosone=child_c, mut_rate=MUTATION_RATE)
                            mut_child_f = mutate(chromosone=child_d, mut_rate=MUTATION_RATE)
                            
                            # Evaluate the fitness of e and f 
                            e_fitness = eval_fitness(chromosone=mut_child_e, weights=weights, values=values, limit=weight_limit)
                            f_fitness = eval_fitness(chromosone=mut_child_f, weights=weights, values=values, limit=weight_limit)

                            # Perform weakest replacment of e and f, respectively, and update population and fitness lists
                            population, fitnesses = weakest_replacment(new_fitness=e_fitness, new_solution=mut_child_e, population=population, fitnesses=fitnesses)
                            population, fitnesses = weakest_replacment(new_fitness=f_fitness, new_solution=mut_child_f, population=population, fitnesses=fitnesses)
                        
                        # Used for brevity
                        max_in_fitnesses = max(fitnesses)

                        # Grab the stats form each trial and add it to a running total to be averaged out when written to the csv file. 
                        # Also keep track of the maximum value found across all 10 trials
                        Min_Fitness_avg += float(min(fitnesses))
                        Max_Fitness_avg += float(max_in_fitnesses)
                        Avg_Fitness_avg += round(float(sum(fitnesses))/float(len(fitnesses)), 2)
                        if max_in_fitnesses > Max_Value_Found:
                            Max_Value_Found = max_in_fitnesses

                    # Write averages and max value found across all the trials to a csv file
                    writer.writerow([POPULATION_SIZE, TOURNAMENT_SIZE, MUTATION_RATE, round(Min_Fitness_avg/NUM_TRIALS, 2), round(Max_Fitness_avg/NUM_TRIALS, 2), round(Avg_Fitness_avg/NUM_TRIALS, 2), Max_Value_Found])
