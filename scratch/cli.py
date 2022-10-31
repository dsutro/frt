#!/usr/bin/python3
# compare.py
import argparse
from fitness import correlate
from listen import spectrogram
import librosa
import matplotlib.pyplot as plt
import librosa.display


def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i ", "--source-file", help="source file")
    parser.add_argument("-o ", "--target-file", help="target file")
    args = parser.parse_args()
  
    SOURCE_FILE = args.source_file if args.source_file else None
    TARGET_FILE = args.target_file if args.target_file else None
    if not SOURCE_FILE or not TARGET_FILE:
      raise Exception("Source or Target files not specified.")
    return SOURCE_FILE, TARGET_FILE
  
if __name__ == "__main__":
    SOURCE_FILE, TARGET_FILE = initialize()
    correlate(SOURCE_FILE, TARGET_FILE)

    # print spectrograms
    # compute spectrogram
    y, sr = librosa.load(TARGET_FILE, sr=None)
    T = spectrogram(y)

    # plot spectrogram
    plt.figure(figsize=(12,3))
    librosa.display.specshow(T, x_axis='time', y_axis='log', sr=sr)
    plt.title('Target Spectrogram')
    plt.show()

    y, sr = librosa.load(SOURCE_FILE, sr=None)
    S = spectrogram(y)

    # plot spectrogram
    plt.figure(figsize=(12,3))
    librosa.display.specshow(S, x_axis='time', y_axis='log', sr=sr)
    plt.title('Source Spectrogram')
    plt.show()

    