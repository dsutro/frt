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
  ga.fitness_func = fitness

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

  data = np.random.uniform(-1, 1, 99600)
  # scaled = np.int16(y / np.max(np.abs(y)) * 32767)
  # write('test.wav', SR, scaled)

  sf.write('test.wav', data, SR, 'PCM_24')

  return 'test.wav'

# def fitness_fnc_euc(target_audio, synth_audio):
#   euc_fnc = lambda x, y: math.sqrt(x**2 - y**2)
#   target_features = mai.listen.spectral_features(target_audio)
#   synth_features = mai.listen.spectral_features(synth_audio)

#   score = 0
#   for key in target_features.keys():
#     score += euc_fnc(target_features[key], synth_features[key])

#   return score

if __name__ == '__main__':
  ga = initialize()

  pop = ga.evolve()