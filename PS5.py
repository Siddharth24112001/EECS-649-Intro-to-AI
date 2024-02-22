import random
import math

EVALS = 0
total_runs = 100
pmut = 0.1
successful_runs = 0

def my_rand(low, high):
    return random.randint(low, high)

def mutate(config, p):
    for i in range(8):
        if random.random() < p:
            config[i] = my_rand(1, 8)

def attacking(q1col, q1row, q2col, q2row):
    if q1row == q2row:
        return 1  # same row
    coldiff = q1col - q2col
    rowdiff = q1row - q2row
    if abs(coldiff) == abs(rowdiff):
        return 1  # same diagonal
    return 0

def fitness(config):
    global EVALS
    EVALS += 1
    fit = 28
    for i in range(8):
        for j in range(i + 1, 8):
            fit -= attacking(i, config[i], j, config[j])
    return fit

def random_config():
    return [random.randint(1, 8) for _ in range(8)]

def print_config(config):
    print(config)

def conflicts(var, config):
    num_conflicts = 0
    for j in range(8):
        if j != var:
            if attacking(var, config[var], j, config[j]):
                num_conflicts += 1
    return num_conflicts

def random_min_conflicts(config, max_steps):
    global successful_runs, EVALS
    for _ in range(max_steps):
        if fitness(config) == 28:
            successful_runs += 1
            return True
        var = my_rand(0, 7)
        while conflicts(var, config) == 0:
            var = my_rand(0, 7)
        min_position = config[var]
        min_conflicts = conflicts(var, config)
        changed_min_conflicts = False
        for i in range(1, 9):
            config[var] = i
            new_num_conflicts = conflicts(var, config)
            if new_num_conflicts < min_conflicts:
                min_position = i
                min_conflicts = new_num_conflicts
                changed_min_conflicts = True
        if not changed_min_conflicts:
            mutate(config, pmut)
        config[var] = min_position
    return False

def cyclic_min_conflicts(config, max_steps):
    global successful_runs, EVALS
    for _ in range(max_steps):
        if fitness(config) == 28:
            successful_runs += 1
            return True
        for var in range(8):
            min_position = config[var]
            min_conflicts = conflicts(var, config)
            changed_min_conflicts = False
            for i in range(1, 9):
                config[var] = i
                new_num_conflicts = conflicts(var, config)
                if new_num_conflicts < min_conflicts:
                    min_position = i
                    min_conflicts = new_num_conflicts
                    changed_min_conflicts = True
            if not changed_min_conflicts:
                mutate(config, pmut)
            config[var] = min_position
    return False

def average_runs(evals, succ):
    cum_evals = sum(evals)
    return math.ceil(cum_evals / succ)

def main():
    global successful_runs, EVALS
    evals_per_run = []
    option = input("Enter 1 for random, 2 for cyclic: ")
    if option == '1':
        for _ in range(total_runs):
            init_config = random_config()
            if random_min_conflicts(init_config, 250):
                print_config(init_config)
                print("NUM EVALS:", EVALS)
                evals_per_run.append(EVALS)
            EVALS = 0
        print("Successful runs:", successful_runs)
        print("Average num evals:", average_runs(evals_per_run, successful_runs))
    elif option == '2':
        for _ in range(total_runs):
            init_config = random_config()
            if cyclic_min_conflicts(init_config, 250):
                print_config(init_config)
                print("NUM EVALS:", EVALS)
                evals_per_run.append(EVALS)
            EVALS = 0
        print("Successful runs:", successful_runs)
        print("Average num evals:", average_runs(evals_per_run, successful_runs))

if __name__ == "__main__":
    main()
