from main import run_ga
import sys
import os
from datetime import datetime
import warnings
from requests import RequestsDependencyWarning
import logging
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RequestsDependencyWarning)
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

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
        'generations': 10,
        'population_size': 10,
        'mutation_prob': 0.5,
        'threshold': 1000
    }
}
    

if __name__ == '__main__':
    directory = '../test_assets'
    # iterate over files
    test_report = {}
    test_begin = datetime.now()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f'\nTesting {f}...\n')
            test_names = list(TEST_DICT.keys())[:1]
            for test_name in test_names:
                print(f"\nRunning {test_name}...\n")
                generations = TEST_DICT[test_name].get('generations')
                population_size = TEST_DICT[test_name].get('population_size')
                mutation_prob = TEST_DICT[test_name].get('mutation_prob')
                threshold = TEST_DICT[test_name].get('threshold')
                min_fitness = run_ga(f, 
                                    generations=generations, 
                                    population_size=population_size, 
                                    mutation_prob=mutation_prob,
                                    verbose=False)['min_fitness']
                print(f'file {f} test {test_name}: {min_fitness}')
                test_report.update({f: {test_name: min_fitness}})
                assert min_fitness <= threshold
    print(f"\n\nTests took {(datetime.now()-test_begin).total_seconds()} seconds to complete\n\n")
    print(test_report)
