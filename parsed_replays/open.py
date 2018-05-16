import numpy as np
import pandas as pd
import csv
from scipy import sparse
import pickle

F = np.asarray(sparse.load_npz('./GlobalFeatureVector/Protoss_vs_Protoss/Protoss/1@0041f867a19b27400acbfb497df38a7ebfb4eec679b3fd30f370fc24c087b096.SC2Replay.npz').todense())
np.savetxt('f.csv', F, delimiter=",", fmt='%s') # .csv is a dataframe

# df = pd.read_csv('file', delimiter=',')
# df.to_csv('file.csv')

with open('f.csv', 'rb') as f:
	file = np.load(f)

# # print(F.shape)
for state in file:
	print(state[317:].mean())
