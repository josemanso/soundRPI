#plot función distorsión fuz hard clippin ccrma.standford.edu
import numpy as np
import matplotlib.pyplot as plt
def distorfuzz(x, g): 
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))

    return y
    
    

x = np.array([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6,0.8,1])
y = np.zeros(len(x))
z = np.zeros(len(x))
v = np.zeros(len(x))
g = 10
y = distorfuzz(x,g)
z = distorfuzz(x,1)
v = distorfuzz(x,5)
print('y ', y)

plt.plot(x,y, label= "gain = 10")
plt.legend()
plt.title('Curva distorsión/fuzz simétrico')
plt.ylabel('output')
plt.xlabel('input')
plt.plot(x,z, label= "gain = 1")
plt.legend()
plt.plot(x,v, label= "gain = 5")
plt.legend()
plt.grid()
            
plt.show()