import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm

from matplotlib import pyplot as PLT, pylab, cm

y1, sr1 = librosa.load('source.wav')  ## signal, sampling rate
y2, sr2 = librosa.load('target.wav')

plt.subplot(1, 2, 1)
mfcc1 = librosa.feature.mfcc(y1, sr1)
librosa.display.specshow(mfcc1)
print("hi")
plt.subplot(1, 2, 2)
mfcc2 = librosa.feature.mfcc(y2, sr2)
librosa.display.specshow(mfcc2)
plt.show()

# calculates distance
# .T is just np.transpose()
dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
# print("mfcc1.T" , dtw(mfcc1.T))
# print(dist,"\n\n", cost,"\n\n", acc_cost,"\n\n", path)
# dist, cost, path = dtw(mfcc1.T, mfcc2.T)
# print(acc_cost)
# dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T)

# dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, lambda x, y: norm(x - y, ord=1))

print('Normalized distance between the two sounds:', dist)

plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, cost.shape[0] - 0.5))
plt.ylim((-0.5, cost.shape[1] - 0.5))
plt.show()
matplotlib.pyplot.show()
