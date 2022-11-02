import genalg
from fitness import fitness
# imports
import synths
import musicfuncs as mf
import time
import matplotlib.pyplot as plt
import random
import math
import librosa
import argparse
import numpy as np
from scipy.io.wavfile import write
import soundfile as sf
from listen import spectral_features


SR = 44100

def initialize():
  """ takes user input """
  parser = argparse.ArgumentParser()
  parser.add_argument("-t ", "--target-file", help="target file")
  args = parser.parse_args()

  target_file = args.target_file if args.target_file else None
  if not target_file:
    raise Exception("Target files not specified.")

  # create a genetic algorithm object
  ga = genalg.GeneticAlgorithm(target_file)
  ga.to_phenotype = to_phenotype
  ga.random_individual = random_individual
  # ga.fitness_func = fitness
  ga.fitness_func = fitness_fnc_euc

  return ga

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
  y = synths.fm(carrier, modulator, index1, index2, attack, release)

  # data = np.random.uniform(-1, 1, 99600)
  # scaled = np.int16(y / np.max(np.abs(y)) * 32767)
  # write('test.wav', SR, scaled)

  sf.write('test.wav', y, SR, 'PCM_24')

  return 'test.wav'

def fitness_fnc_euc(synth_fname, target_features):
  # euc_fnc = lambda x, y: (x**2 - y**2)
  euc_fnc = lambda x, y: math.sqrt(sum([(xx - yy)**2 for xx, yy in zip(x, y)]))
  synth_features = spectral_features(synth_fname)

  score = 0
  for key in target_features.keys():
    cut_i = min(len(synth_features[key]), len(target_features[key]))
    # TODO: penalize len diff
    # len_dif = max(len(synth_features), len(target_features)) - min(len(synth_features), len(target_features))

    score += euc_fnc(target_features[key][:cut_i], synth_features[key][:cut_i])

  score = (score / len(target_features.keys()))
  print(score)
  return score

if __name__ == '__main__':
  ga = initialize()

  pop = ga.evolve(population_size=10)
  # feats = spectral_features('test.wav')
  # for key in feats.keys():
  #   print(len(feats[key]))

  

