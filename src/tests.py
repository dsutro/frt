from main import test_ga, run_ga
import sys
import os

TEST_DICT = {
    'test1': {
        'generations': 10,
        'population_size': 10,
        'mutation_prob': 0.01,
        'threshold': 1000
    },
    'test2': {
        'generations': 10,
        'population_size': 10,
        'mutation_prob': 0.05,
        'threshold': 1000
    },
    'test3': {
        'generations': 10,
        'population_size': 10,
        'mutation_prob': 0.1,
        'threshold': 1000
    },
    'test4': {
        'generations': 15,
        'population_size': 20,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test5': {
        'generations': 5,
        'population_size': 17,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test5': {
        'generations': 17,
        'population_size': 5,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test6': {
        'generations': 15,
        'population_size': 20,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test7': {
        'generations': 15,
        'population_size': 20,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test8': {
        'generations': 15,
        'population_size': 20,
        'mutation_prob': 0.1,
        'threshold': 1000
    },
    'test9': {
        'generations': 15,
        'population_size': 20,
        'mutation_prob': 0.07,
        'threshold': 1000
    },
    'test10': {
        'generations': 12,
        'population_size': 18,
        'mutation_prob': 0.06,
        'threshold': 1000
    }
}
    

if __name__ == '__main__':
    directory = '../test_assets'
    # iterate over files
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f'\nTesting {f}...\n')
            test_names = list(TEST_DICT.keys())[:3]
            for test_name in test_names:
                print(f"\nRunning {test_name}...\n")
                generations = TEST_DICT[test_name].get('generations')
                population_size = TEST_DICT[test_name].get('population_size')
                mutation_prob = TEST_DICT[test_name].get('mutation_prob')
                threshold = TEST_DICT[test_name].get('threshold')
                min_fitness = test_ga(f, generations=generations, population_size=population_size, mutation_prob=mutation_prob)
                print(f'file {f} test {test_name}: {min_fitness}')
                assert min_fitness <= threshold

# test_assets dir:
# 	for each file:
# 		generations = [5, 10, 25]
# 		population_size = [5, 10, 25]
# 		mutation_pob = [0.01, 0.05, 0.1]
# 		assert min_fitness < THRESHOLD

# test_name: {'generations':5, 'population': 5, 'threshold': 1000}