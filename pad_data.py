import numpy as np 
import pickle
from prep_data import units, terran_x, terran_y, dict_map


def pad_and_batch(data, batch_size=50):
	temp = []
	for d in data:
		x = d[0]
		y = d[1]
		y = np.array([int(yy[0]) for yy in y])

		if len(x) == batch_size:
			temp.append((x, y))
		elif len(x) < batch_size:
			pad_size = batch_size - len(x)
			pad = np.zeros((pad_size, x.shape[1]))
			ped = np.zeros((batch_size - len(y),1))
			padded = np.vstack((x, pad))
			pepped = np.vstack((y.reshape((y.shape[0], 1)), ped))
			temp.append((padded, pepped))
		else:
			start = 0
			##print(len(x))
			for indx in range(batch_size, len(x)+batch_size, batch_size):
				#print('...',indx)
				if start+batch_size < len(x):
					#print("XXX ", x[start:indx].copy())
					temp.append((x[start:indx].copy().astype(int), y[start:indx].copy()))
				else:
					pad_size = batch_size - len(x[start:])
					pad = np.zeros((pad_size, x.shape[1]))
					ped = np.zeros((batch_size - len(y[start:]),))
					padded = np.vstack((x[start:].copy(), pad)).astype(int)
					pepped = np.hstack((y[start:].copy(), ped)).astype(int)
					temp.append((padded, pepped))
				start = indx
	return temp

if __name__ == '__main__':
	with open('preped_data.pkl', 'rb') as preped:
		data = pickle.load(preped)
	new_data = pad_and_batch(data)
	##with open('preped_maps.pkl', 'rb') as maps:
	##	mapped = pickle.load(maps)
	##for a in sorted(mapped):
	##	print(a, mapped[a])
