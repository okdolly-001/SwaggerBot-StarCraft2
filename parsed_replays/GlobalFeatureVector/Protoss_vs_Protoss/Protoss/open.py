import os
import numpy as np
from scipy import sparse

PATH = '/Users/domore/SwaggerBot-StarCraft2/parsed_replays/GlobalFeatureVector/Protoss_vs_Protoss/Protoss/'
filenames = os.listdir(PATH)
game1 = filenames[0]
data = np.asarray(sparse.load_npz(PATH+game1).todense())

print(data)