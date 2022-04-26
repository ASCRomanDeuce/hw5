import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import example4
import imageio as iio
import sys

class solver:
    def __init__(self, N, h, m):
        #N size, h step, m number of  max iterations,
        #w is coeff in SOR method, iterations is final number of uterations
        self.N, self.h, self.m = N, h, m
        self.epsilon = 0.01
        self.w=1 #w_opt=1.935-->152iterations
        self.rho=0.1
        self.iterations=0
        self.U_old = np.zeros((N,N))
        self.U_old[0, :] = 100
        self.U_old[N-1,:]=0
        self.U_new=np.copy(self.U_old)
        self.pos = iio.imread('1.png')[:,:,0]
        #self.neg = iio.imread('2.png')[:,:,0]
        #self.pos = np.zeros((N,N))
        self.neg = np.zeros((N,N))
        np.set_printoptions(threshold=sys.maxsize)
        c=self.pos-self.neg
        
        #print(self.pos-self.neg)
        
    def condition(self):
        arr=self.U_new
        arr_old=self.U_old
        N=self.N
        for i in range(self.m):
            #изменяю размерность массива, теперь он 1*0 вместо N*N.
            arr_old=arr_old.flatten()
            arr = arr.flatten()
            #Пробегаю по всем точкам с помощью срезов
            arr[N+1:N*N-N-2]= ( arr_old[1:N*N-2*N-2]+arr_old[N:N*N-N-3]+arr_old[N+2:N*N-N-1]+arr_old[2*N+1:N*N-2] )/4
            #Возвращаю старую размерность N*N и задаю условие на границе, которое остается const
            arr=arr.reshape((N,N))
            arr[N-1, :]=0
            arr[:, 0]=0
            arr[:, N-1]=0
            arr[0 :] = 100
            #проверяю норму каждые 4 итерации 
            if i // 4 == i/4 and self.norm(arr,arr_old.reshape(N,N))<self.epsilon:
                self.iterations=i
                break
            
            arr_old = arr
            
        self.U_new = arr.reshape((N,N))
        self.iterations=i


    def condition__2(self):
        self.U_new, self.iterations =example4.condition_2(self.U_old, self.N, self.m,self.norm, \
                                                          self.epsilon, self.w,self.rho, self.h, \
                                                          self.pos, self.neg)

    def plotter (self):
        h=self.h
        N=self.N
        i=self.iterations
        data=np.arange(0, N*h, h)
        #поле значений должно иметь вид
        #0,0 0,h ... 0,L
        #...
        #L,0 L,h ... L,L
        # поэтому x имеет сначала повт. значения каждого элемента из data N раз, а y повторяет data целиком N раз
        X = np.repeat(data,N)
        Y = np.tile(data,N)
        Z = self.U_new.flatten()
        
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        X, Y = np.meshgrid(data, data)
        Z=self.U_new
        #3d plot
        ax.set_title('3d plot + equipotential lines, iter number = %i' %i)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha = 0.5,
                       linewidth=0, antialiased=False)
        Ex,Ey=self.E_field(self.U_new)
        
        plt.show()
        #2d plot
        fig, ax = plt.subplots()
        CS = ax.contour(X, Y, self.U_new)
        c=ax.streamplot(data, data, Ey, Ex, linewidth=1, 
              density=2, arrowstyle='->', arrowsize=1.5)
        ax.clabel(CS, inline=True, fontsize=10)
        ax.set_title('equipotential lines  with labels, iter number = %i' %i)
        fig.show()

    def norm(self,a,b):
        z=(a-b)*(a-b)
        return np.sqrt(np.sum(z))
    
    def E_field(self,a):
        N=self.N
        Ex = np.zeros((N,N))
        Ey = np.zeros((N,N))
        for (i,j), x in np.ndenumerate(Ex):
            if i == 0 or i == N-1 or j == 0 or j == N-1:
                continue
            Ex[i,j]=( a[i+1,j]-a[i-1,j] )/(2 * self.h)
        for (i,j), x in np.ndenumerate(Ey):
            if i == 0 or i == N-1 or j == 0 or j == N-1:
                continue
            Ey[i,j]=( a[i,j+1]-a[i,j-1] )/(2 * self.h)
        
        return -Ex,-Ey
            
        


        
          
x=solver(50, 1, 5000)
x.condition__2()
x.plotter()
