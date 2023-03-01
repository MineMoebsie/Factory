import numpy as np

array_np = np.zeros((500,500),dtype="str")
#print(array_np)

f = open("Data/WriteFiles/wereld_2/craft_grid.txt",'w')
np.savetxt(f, array_np.reshape((1,-1)), fmt="%s")
f.close()



loaded_array = np.loadtxt('Data/WriteFiles/wereld_2/craft_grid.txt').reshape(500, 500)
loaded_array = loaded_array.astype(str)

print(loaded_array)