#!/usr/bin/python3

import subprocess
import numpy
import os


# seconds to sample audio file for
sample_time = 5
# number of points to scan cross correlation over
span = 11
# step size  of cross correlation
step = 1

# minimum number of points that must overlap in cross correlation
MIN_OVERLAP = 1

# report match when cross correlation has a peak exceeding THRESHOLD
THRESHOLD = 0.5

# calculate fingerprint
# Generate file.mp3.fpcalc by "fpcalc -raw -length 500 file.mp3"
def calculate_fingerprints(filename):
    if os.path.exists(filename + '.fpcalc'):
        print("Found precalculated fingerprint for %s" % (filename))
        f = open(filename + '.fpcalc', "r")
        fpcalc_out = ''.join(f.readlines())
        f.close()
    else:
        print("Calculating fingerprint by fpcalc for %s" % (filename))
        fpcalc_out = str(subprocess.check_output(['fpcalc', '-raw', '-length', str(sample_time), filename])).strip().replace('\\n', '').replace("'", "")

    fingerprint_index = fpcalc_out.find('FINGERPRINT=') + 12
    # convert fingerprint to list of integers
    fingerprints = list(map(int, fpcalc_out[fingerprint_index:].split(',')))
    
    return fingerprints
  
# returns correlation between lists
def correlation(listx, listy):
    if len(listx) == 0 or len(listy) == 0:
        raise Exception('Empty lists cannot be correlated.')
    if len(listx) > len(listy):
        listx = listx[:len(listy)]
    elif len(listx) < len(listy):
        listy = listy[:len(listx)]
    
    covariance = 0
    for i in range(len(listx)):
        covariance += 32 - bin(listx[i] ^ listy[i]).count("1")
    covariance = covariance / float(len(listx))
    
    return covariance/32
  
# return cross correlation, with listy offset from listx
def cross_correlation(listx, listy, offset):
    if offset > 0:
        listx = listx[offset:]
        listy = listy[:len(listx)]
    elif offset < 0:
        offset = -offset
        listy = listy[offset:]
        listx = listx[:len(listy)]
    if min(len(listx), len(listy)) < MIN_OVERLAP:
        # Error checking in main program should prevent us from ever being
        # able to get here.
        print(f"Min overlap ({MIN_OVERLAP}) not met by {(lambda: 'Target', lambda: 'Source')[min(len(listx), len(listy)) == len(listx)]()}")
        return 
    #raise Exception('Overlap too small: %i' % min(len(listx), len(listy)))
    return correlation(listx, listy)
  
# cross correlate listx and listy with offsets from -span to span
def compare(listx, listy, span, step):
    if span > min(len(listx), len(listy)):
        # Error checking in main program should prevent us from ever being
        # able to get here.
        raise Exception('span >= sample size: %i >= %i\n'
                        % (span, min(len(listx), len(listy)))
                        + 'Reduce span, reduce crop or increase sample_time.')
    corr_xy = []
    for offset in numpy.arange(-span, span + 1, step):
        corr_xy.append(cross_correlation(listx, listy, offset))
    return corr_xy
  
# return index of maximum value in list
def max_index(listx):
    max_index = 0
    max_value = listx[0]
    for i, value in enumerate(listx):
        if value > max_value:
            max_value = value
            max_index = i
    return max_index
  
def get_max_corr(corr, source, target):
    max_corr_index = max_index(corr)
    max_corr_offset = -span + max_corr_index * step
    #print("max_corr_index = ", max_corr_index, "max_corr_offset = ", max_corr_offset)
    # report matches
    if corr[max_corr_index] > THRESHOLD:
        print("Source: %s" % (source))
        print("Target: %s" % (target))
        print('Match with correlation of %.2f%% at offset %i'
             % (corr[max_corr_index] * 100.0, max_corr_offset))
        return corr[max_corr_index], max_corr_offset

def fitness(source, fingerprint_target):
    try:
        fingerprint_source = calculate_fingerprints(source)

        corr = compare(fingerprint_source, fingerprint_target, span, step)
        max_corr, max_offset = get_max_corr(corr, source, target)
        return max_corr
    except Exception as e:
        print(f'fitness calc failed due {e}')
        if e.find('Command') != 1:
            exit()
    return 0 

def correlate(source, target):
    fingerprint_source = calculate_fingerprints(source)
    fingerprint_target = calculate_fingerprints(target)

    corr = compare(fingerprint_source, fingerprint_target, span, step)
    max_corr, max_offset = get_max_corr(corr, source, target)
    return max_corr