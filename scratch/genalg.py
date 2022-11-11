import random
import functools
import matplotlib.pyplot as plt
import numpy as np
import copy
import librosa
import numpy as np
from scipy.io.wavfile import write
import soundfile as sf
from multiprocessing import Pool

# local
from listen import spectral_features
from fitness import fitness, calculate_fingerprints
import synths
from listen import spectral_features
import musicfuncs as mf

# global ---------------------


# default functions ----------------------------------------------------------------------

def random_individual():
    """Generate a random individual phenotype"""

    return [random.randrange(0,2) for i in range(10)]

def to_phenotype(genotype):
    return genotype

def to_weight(fitness, m=100, b=1):
    """Convert from fitness score to probability weighting"""

    return int(round(fitness*m + b))

def reproduce(parent1, parent2):
    """generate offspring using random crossover"""

    # random crossover point
    crossover = random.randrange(0, len(parent1))

    # construct children
    child1 = parent1[0:crossover] + parent2[crossover:]
    child2 = parent2[0:crossover] + parent1[crossover:]

    # return children
    return child1, child2

def mutate(genotype, mutation_prob=0.01, inbreeding_prob=0.5, verbose=True):
    """Mutate!"""

    # do we mutate?
    if random.random() <= mutation_prob:

        # print it
        if verbose: print('-> muuuuutating individual {0}'.format(genotype))

        # select a random chromosome
        gene_index = random.randrange(len(genotype))

        # flip its value
        genotype[gene_index] = 1 - genotype[gene_index]

    return genotype

def fitness_job(self, iter, i):
    """Fitness job to run fitness function in parallel"""
    fname = f"temp/temp_audio_gen_{iter}_"
    self.fitness[i] = (self.fitness_func(self.to_phenotype(self.population[i], self.duration, self.sr, fname), self.target_features), self.population[i])

# genetic algorithm  ---------------------------------------------------------------------

class GeneticAlgorithm:
    """A very simple Genetic Algorithm."""

    def __init__(self, target_fname):

        # initialize default functions
        self.random_individual = random_individual
        self.fitness_func = fitness
        self.to_phenotype = to_phenotype
        self.to_weight = to_weight
        self.reproduce = reproduce
        self.mutate = mutate
        self.target_fname = target_fname
        self.target_fingerprint = None
        self.target_features = None
        self.sr = 44100

        # try to get target features
        try:
            self.target_features = spectral_features(target_fname)
            self.duration = librosa.get_duration(filename=target_fname)
        except Exception as e:
            print(f'Genetic Algorithm initialization failed due to : {e}')

    def initialize_population(self, population_size=10):
        """Initialize the population."""

        # store population size
        self.population_size = population_size

        # initialize individuals
        self.population = [self.random_individual() for i in range(population_size)]
        self.generations = [copy.copy(self.population)]

        # initialize fitness to 0 for all
        self.fitness = [[0, individual] for individual in self.population]



    def evolve(self, iters=10, population_size=100, init_pop=True, mutation_prob=0.01):
        """Run the GA."""

        # initialize the population
        if init_pop or self.population == None:
            self.population_size = population_size
            self.population = [self.random_individual() for i in range(population_size)]
            self.generations = [copy.copy(self.population)]
            self.fitness = [[0, individual] for individual in self.population]

        # loop iters times
        for iter in range(iters):

            # spectral features fitness 
            arg1 = [self]*self.population_size
            arg2 = [iter]*self.population_size
            arg3 = [i for i in range(population_size)]
            with Pool(4) as p:
                p.starmap(fitness_job, zip(arg1, arg2, arg3))

            # adjust fitness (when using spectral features)
            max_fitness = max([self.fitness[i][0] for i in range(self.population_size)])
            print(f"Max Fitness: {max_fitness}")
            for i in range(self.population_size):
                self.fitness[i] = list(self.fitness[i])
                self.fitness[i][0] = 1 - (self.fitness[i][0] / max_fitness)

            # construct mating pool of probabilities weighted by fitness score
            mating_pool = functools.reduce(lambda x,y: x+y, [[individual]*self.to_weight(score)
                                                   for (score,individual) in self.fitness])

            # select population_size/2 pairs of parents from the mating pool
            parents = [(random.choice(mating_pool), random.choice(mating_pool))
                       for i in range(int(population_size/2))]

            # generate new offspring from parents
            offspring = functools.reduce(lambda x,y: x+y, [self.reproduce(parent1, parent2)
                                                 for (parent1,parent2) in parents])

            # mutate
            map(lambda x: self.mutate(x, mutation_prob=mutation_prob), offspring)

            # update the population
            self.population = offspring
            self.generations += [copy.copy(self.population)]
            print(f'iter: {iter}')

        return self.population

    def evolve_once(self, mutation_prob=0.01):
        """Evolve one generation using fitness scores in self.fitness."""

        # construct mating pool of probabilities weighted by fitness score
        mating_pool = functools.reduce(lambda x,y: x+y, [[individual]*self.to_weight(score)
                                               for (score,individual) in self.fitness])

        # select population_size/2 pairs of parents from the mating pool
        parents = [(random.choice(mating_pool), random.choice(mating_pool))
                   for i in range(int(self.population_size/2))]

        # generate new offspring from parents
        offspring = functools.reduce(lambda x,y: x+y, [self.reproduce(parent1, parent2)
                                             for (parent1,parent2) in parents])

        # mutate
        offspring = [self.mutate(x, mutation_prob=mutation_prob) for x in offspring]

        # update the population
        self.population = offspring
        self.generations += [copy.copy(self.population)]

        # update individuals in the fitness
        self.fitness = [[0, individual] for individual in self.population]

    def set_fitness(self, score, individual=0):
        """Set individual fitness score."""

        # update fitness score
        self.fitness[individual][0] = score


    def plot_generations(self, start=0, end=6, all=False):
        """Plot generations."""

        if not all:

            gens = self.generations[start:end]
            num_gens = len(gens)

            fig, axes = plt.subplots(nrows=1, ncols=num_gens)

            for i,gen in enumerate(gens):
              axes[i].imshow(np.array(gen), cmap='gray_r')

            for i,ax in enumerate(axes):
                ax.set_xticks([])
                ax.set_yticks([])
                if i == 0:
                    ax.set_ylabel('Individuals')
                ax.set_xlabel('Genotypes')
                ax.set_title('Gen {}'.format(i))

            plt.tight_layout()
            plt.show()

        if all:

            alpha = np.array(self.generations)
            alpha = np.swapaxes(alpha, 1, 2)
            n_iters, geno_len, pop_size = alpha.shape

            alpha_hat = np.reshape(alpha, (n_iters * geno_len, pop_size)).T

            plt.imshow(alpha_hat, cmap='gray_r', aspect='auto')
            ax = plt.gca()
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_ylabel('Individuals')
            ax.set_xlabel('Genotypes by Generation')
            ax.set_title('Generations')
            plt.show()


def plot_genotype(genotype):
    """Plot genotype as matrix."""
    plt.figure(figsize=(3,0.5))
    plt.imshow(np.atleast_2d(np.array(genotype)), cmap='gray_r')
    plt.xticks([])
    plt.yticks([])
    plt.show()


def test_GA():
    ga = GeneticAlgorithm()
    ga.evolve(10, init_pop=True, mutation_prob=0.01)
    return ga
