import random


def get_weight_limit(line):
    """
    Simply returns the cleaned weight limit as an integer from teh first line of the document
    """
    return int(line.split(':')[1])


def init_pop(weights, pop_size):
    '''
    Generate a population of random solutions.

    params:
    weights: list containing all weights of the bags
    pop_size: int defining how many solutions to make

    return: list of lists which are the pop_size solutions
    '''
    solutions = []
    
    for i in range(pop_size):
        # Reset temp solution
        temp_solution = []
        for i in range(len(weights)):
            # Each bag has a 50/50 chance of being chosen to be part of any solutions
            rand_num = random.randint(0, 100)
            if rand_num > 50:
                # Add bag to solution
                temp_solution.append(1)
            else:
                # Do not add bag to solution
                temp_solution.append(0)
        # Add temp_solution to populations
        solutions.append(temp_solution)
    
    return solutions


def eval_fitness(chromosone, weights, values, limit):
    '''
    Fitness function that evaluates fitness based on total value of all the bags in the solution. Returns zero if weight exceeds limit

    params:
    chromosone: list with the current solution being evaluated
    weights: list of all the weights of the bags
    values: list of all values of the bags
    limit: integer denoting weight limit of van

    return: int total value of the solution
    '''
    cur_weight = 0
    cur_value = 0

    # evaluate each gene and if the bag at that index is included, then add its' weight and value to the running total
    for i in range(len(chromosone)):
        if chromosone[i]:
            cur_weight += weights[i]
            cur_value += values[i]
        else:
            continue

    # Solutions exceeding limit will be penalised with a fitness of 0
    if cur_weight > limit:
        return 0
    else:
        return cur_value


def tournament_select(fitnesses, tourney_size):
    '''
    Selects a number of chromosones in the populaiton and returns the fittest

    params:
    fitnesses: list of the fitnesses of the current populaiton
    tourney_size: int the number of chromosones considered

    return: int index of the fittest solution in the tourney
    '''
    participants = []
    cur_highest = 0
    cur_highest_ind = 0

    # Runs until required number of unique participants is obtained
    # while len(participants) < tourney_size:
    #     rand_ind = random.randint(0, len(fitnesses)-1)
    #     if rand_ind in participants:
    #         continue
    #     else:
    #         participants.append(rand_ind)

    participants = random.sample(range(len(fitnesses)-1), tourney_size)

    # Evaluate which of the participants is the fittest
    for participant in participants:
        if fitnesses[participant] > cur_highest:
            # If the fitness of teh current participant is greater than teh current leader, then adjust new values
            cur_highest = fitnesses[participant]
            cur_highest_ind = participant
    
    return cur_highest_ind


def crossover(parent1, parent2, co):
    '''
    Performs simple 1-point crossover on two parents to produce two children

    params:
    parent1: list containing first parent chromosone
    parent2: list ocntaining second parent chromosone
    co: int index denoting crossover point

    return: two lists children of post crossover
    '''

    child_c = []*len(parent1)
    child_d = []*len(parent1)

    child_c[:co] = parent1[:co]
    child_c[co:] = parent2[co:]

    child_d[:co] = parent2[:co]
    child_d[co:] = parent1[co:]

    return child_c, child_d


def mutate(chromosone, mut_rate):
    '''
    Each gene has a mut_rate chance of being mutated (i.e. 0->1 or 1->0)

    params:
    chromosone: list the chromosone being mutated
    mut_rate: int the chance (%) of each gene being mutated

    return: list chromosone that has gone through mutation
    '''
    mutatie = []
    for i in range(len(chromosone)):
        # This gives each gene a mut_rate chance of being mutated
        if random.randint(0, 100) <= mut_rate:
            if chromosone[i] == 0:
                mutatie.append(1)
            elif chromosone[i] == 1:
                mutatie.append(0)
        else: 
            # Append to mutatie regardless to keep indexing consistent
            mutatie.append(chromosone[i])
    
    return mutatie

def weakest_replacment(new_fitness, new_solution, population, fitnesses):
    '''
    Take the new fitness and compare to the current population fitnesses, if it's higher than the lowest current fitness, replace. Else, discard

    params:
    new_fitness: integer fitness value of new chromosone
    new_solution: list new chromosone 
    population: list of lists current chromosones in the working population
    fitnesses: list of ints denoting current working populace fitensses 

    return: two lists updated population with relevant fitnesses
    '''
    # Will grab the first lowest fitness in the curretn fitnesses list
    cur_fit_min = min(fitnesses)
    if cur_fit_min > new_fitness:
        return population, fitnesses
    else:
        ind = fitnesses.index(cur_fit_min)
        fitnesses[ind] = new_fitness
        population[ind] = new_solution
        #print(f"Replaced solution: {ind}")
    
    return population, fitnesses

