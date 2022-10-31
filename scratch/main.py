import genalg
from fitness import _correlate
# imports
import mai.synths
import mai.musifuncs as mf
import IPython.display
import time
import matplotlib.pyplot as plt
import random
import math
import librosa
import argparse

def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t ", "--target-file", help="target file")
    args = parser.parse_args()
  
    TARGET_FILE = args.target_file if args.target_file else None
    if not TARGET_FILE:
      raise Exception("Target files not specified.")
    return TARGET_FILE

def random_individual():
  """Generate random genotype 6 values in range [0,1]."""
  
  # create a random genotype
  genotype = [random.random() for i in range(6)]

  # return it
  return genotype

def to_phenotype(genotype):
  """Convert genotype to sound using FM synthesis."""
    
  # scale values
  carrier   = mf.scale(genotype[0], 1, 10000, kind='exp')  # carrier freq
  modulator = mf.scale(genotype[1], 1, 10000, kind='exp')  # modulator freq 
  index1    = mf.scale(genotype[2], 1, 100, kind='exp')    # index start
  index2    = mf.scale(genotype[3], 1, 100, kind='exp')    # index end
  attack    = mf.scale(genotype[4], 0.01, 5, kind='exp')   # attack
  release   = mf.scale(genotype[5], 0.01, 5, kind='exp')   # release
  
  # synthesize audio using FM synthesis
  y = mai.synths.fm(carrier, modulator, index1, index2, attack, release)
  
  return y

euc_fnc = lambda x, y: math.sqrt(x**2 - y**2)

def fitness_fnc(target_audio, synth_audio):
  target_features = mai.listen.spectral_features(target_audio)
  synth_features = mai.listen.spectral_features(synth_audio)

  score = 0
  for key in target_features.keys():
    score += euc_fnc(target_features[key], synth_features[key])

  return score

if __name__ == '__main__':
    TARGET_FILE = initialize()

    print("initializing ga")
    # create a genetic algorithm object
    ga = mai.genalg.GeneticAlgorithm()

    # overwrite default function 
    ga.to_phenotype = to_phenotype

    # overwrite default function 
    ga.random_individual = random_individual

    # overwrite fitness func
    ga.fitness_func = _correlate

    # initialize random population
    ga.initialize_population(population_size=12)

    print('loading audio')
    filename = TARGET_FILE
    target_audio, sr = librosa.load(filename, sr=None)

    # first gen
    for i,genotype in enumerate(ga.population):

        print('sounding individual {0}'.format(i))
            
        # convert to phenotype
        y = ga.to_phenotype(genotype)
            
        # play it
        # d = IPython.display.Audio(y, rate=44100, autoplay=False)
        # d = IPython.display.Audio(y, rate=sr, autoplay=False)
        # IPython.display.display(d)

        ga.fitness[i][0] = _correlate(target_audio, y)
        
    # evolve next generation
    ga.evolve_once(mutation_prob=0.1)

    print(ga.fitness)