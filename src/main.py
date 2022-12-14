import genalg
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
from dtw import dtw
from numpy.linalg import norm
from scipy.io.wavfile import write
import soundfile as sf
from listen import spectral_features
import pytest
import glob
import os

def random_individual():
  """Generate random genotype 6 values in range [0,1]."""
  
  # create a random genotype
  genotype = [random.random() for i in range(5)]

  # return it
  return genotype

def to_phenotype(individual, genotype, duration, sr, fname='temp_audio'):
        """Convert genotype to sound using FM synthesis."""
            
        # scale values
        carrier   = mf.scale(genotype[0], 1, 10000, kind='exp')  # carrier freq
        modulator = mf.scale(genotype[1], 1, 10000, kind='exp')  # modulator freq 
        index1    = mf.scale(genotype[2], 1, 100, kind='exp')    # index start
        # index2    = mf.scale(genotype[3], 1, 100, kind='exp')    # index end
        attack    = mf.scale(genotype[3], 0.01, 5, kind='exp')   # attack
        release   = mf.scale(genotype[4], 0.01, 5, kind='exp')   # release

        # randomly use attack or release to ensure target duration
        check = random.random()
        if (check > 0.5):
            release = abs(duration - attack)
        else:
            attack = abs(duration - release)

        # print(f"dur:{duration}\nsr: {sr}\natt: {attack}\nrel: {release}\ncarrier: {carrier}\nmod: {modulator}\nindex: {index1}")
        
        # synthesize audio using FM synthesis
        y = synths.fm(carrier=carrier, modulator=modulator, index1=index1, 
                        index2=0, attack=attack, release=release)
      
        fname = fname + f"{individual}.wav"
        sf.write(fname, y, sr, 'PCM_24')
        return fname

def to_params(genotype, duration, sr):
        """Convert genotype to sound using FM synthesis."""
            
        # scale values
        carrier   = mf.scale(genotype[0], 1, 10000, kind='exp')  # carrier freq
        modulator = mf.scale(genotype[1], 1, 10000, kind='exp')  # modulator freq 
        index1    = mf.scale(genotype[2], 1, 100, kind='exp')    # index start
        # index2    = mf.scale(genotype[3], 1, 100, kind='exp')    # index end
        attack    = mf.scale(genotype[3], 0.01, 5, kind='exp')   # attack
        release   = mf.scale(genotype[4], 0.01, 5, kind='exp')   # release

        # randomly use attack or release to ensure target duration
        check = random.random()
        if (check > 0.5):
            release = abs(duration - attack)
        else:
            attack = abs(duration - release)

        return carrier, modulator, index1, attack, release

def fitness_fnc_euc(synth_fname, target_features):
  # euc_fnc = lambda x, y: (x**2 - y**2)
  euc_fnc = lambda x, y: math.sqrt(sum([(xx - yy)**2 for xx, yy in zip(x, y)]))
  synth_features = spectral_features(synth_fname)

  score = 0
  # for key in target_features.keys():
  for key in ['lowlevel.spectral_centroid', 'lowlevel.spectral_energy', 'lowlevel.spectral_kurtosis', 'lowlevel.spectral_rms']:
    cut_i = min(len(synth_features[key]), len(target_features[key]))
    # TODO: penalize len diff
    # len_dif = max(len(synth_features), len(target_features)) - min(len(synth_features), len(target_features))

    score += euc_fnc(target_features[key][:cut_i], synth_features[key][:cut_i])

  score = (score / len(target_features.keys()))
  # print(score)
  return score

def fitness_fnc_dtw(synth_fname, target_mfcc):
  synth, sr = librosa.load(synth_fname)
  synth_mfcc = librosa.feature.mfcc(synth, sr)
  dist, cost, acc_cost, path = dtw(synth_mfcc.T, target_mfcc.T, dist=lambda x, y: norm(x - y, ord=1))
  return dist

def run_ga(target_fname, generations=10, population_size=10, mutation_prob=0.05, verbose=False):
  """Wrapper to run GA from flask"""
  # create a genetic algorithm object
  ga = genalg.GeneticAlgorithm(target_fname)
  ga.to_phenotype = to_phenotype
  ga.random_individual = random_individual
  ga.fitness_func = (fitness_fnc_dtw, fitness_fnc_euc)
  pop = ga.evolve(iters=generations, population_size=population_size, mutation_prob=mutation_prob)

  # return best set of params
  fitness = [individual[0] for individual in pop]
  individual = fitness.index(min(fitness))
  carrier, modulator, index1, attack, release = to_params(pop[individual], ga.duration, ga.sr)
  params = {'carrier': carrier, 
            'modulator': modulator, 
            'index': index1,
            'attack': attack,
            'release': release,
            'individual': individual}
  # cleanup
  if verbose: print("Cleaning up...")
  files = glob.glob('../tmp/*/.wav', recursive=True)
  for f in files:
      try:
          os.remove(f)
      except OSError as e:
          if verbose: print("Error: %s : %s" % (f, e.strerror))
  
  return params

def test_ga(target_fname, generations=10, population_size=10, mutation_prob=0.05, verbose=False):
  # create a genetic algorithm object
  ga = genalg.GeneticAlgorithm(target_fname)
  ga.to_phenotype = to_phenotype
  ga.random_individual = random_individual
  ga.fitness_func = (fitness_fnc_dtw, fitness_fnc_euc)
  pop = ga.evolve(iters=generations, population_size=population_size, mutation_prob=mutation_prob)

  # cleanup
  files = glob.glob('../tmp/*/.wav', recursive=True)
  for f in files:
      try:
          os.remove(f)
      except OSError as e:
          if verbose: print("Error: %s : %s" % (f, e.strerror))

  return min([individual[0] for individual in pop])


if __name__ == '__main__':
  params = run_ga('../assets/sine.wav')
  # print(params)

  
