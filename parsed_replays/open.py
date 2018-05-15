import numpy as np
import pandas as pd
import csv
from scipy import sparse

F = np.asarray(sparse.load_npz('./GlobalFeatureVector/Protoss_vs_Protoss/Protoss/1@0041f867a19b27400acbfb497df38a7ebfb4eec679b3fd30f370fc24c087b096.SC2Replay.npz').todense())
np.savetxt('file', F, fmt='%s') # .csv is a dataframe

df = pd.read_csv('file', delimiter=' ')
df.to_csv('file.csv')

print(F.shape)
#for state in F:
# 	print(state[317:].mean())
