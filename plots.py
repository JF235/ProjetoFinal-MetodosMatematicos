import numpy as np
from numpy import deg2rad, sqrt, pi, sin, cos
from numpy.linalg import norm
from scipy.optimize import newton
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt

MU = 3.986004418E5
C = 300 # km/ms

def perifocalPos(tp, a, e, mu = MU):
    
    def kepler(E, M, e):
        # Equação de Kepler na forma: f(E) = 0
        return E - e * sin(E) - M

    def dKepler(E, M, e):
        # Derivada da Equação de Kepler f'(E)
        return 1 - e * cos(E)

    tp = np.atleast_1d(tp)
    
    T = 2 * pi / sqrt(mu) * a**(3 / 2) # Período Orbital (seg)
    M = (2*pi/T * tp) % (2*pi) # Anomalia Média

    # Resolve a Equação de Kepler para a Anomalia Excêntrica
    E0 = M
    E = newton(func=kepler, x0=E0, fprime=dKepler, args=(M, e))
    
    # Resposta do item a)
    x = a*cos(E) - a*e
    y = a*sqrt(1-e**2)*sin(E)
    
    return np.array([x, y])

def posVec(tp, a, e, w, i, o, mu = MU):
    pPos = perifocalPos(tp, a, e, mu)
    
    perifocal3D = np.vstack([pPos, np.zeros(pPos.shape[1])])
    
    # Realiza as três rotações
    angles = -np.array([w, i, o]).T
    angles = deg2rad(angles)
    R = Rotation.from_euler("ZXZ", angles).as_matrix()
    pos = R.T @ perifocal3D

    return pos

def grad(x):
    # satPos, rho são variáveis globais
    d = x - satPos
    rhoHat = norm(d, axis=1)
    return d.T @ (1 - rho/rhoHat)

def gradient_descent(grad, x0, Nsteps=200, learningRate=0.6, momentum=0.7):
    x = x0
    vel = np.array([[0, 0, 0]], dtype='float64')
    
    for _ in range(Nsteps):
        g = grad(x)
        
        vel = momentum * vel - learningRate * g
        x += vel
    
    return x

def plot1():
    ax.scatter(satPos[:, 0], satPos[:, 1], satPos[:, 2])
    for x, y, z in zip(satPos[:, 0], satPos[:, 1], satPos[:, 2]):
            ax.text(x, y, z, "🛰️", fontdict=dict(fontfamily="Segoe UI Emoji"))
    ax.scatter(-6420., -6432.,  6325.)
    ax.text(-6420., -6432.,  6325., "📡", fontdict=dict(fontfamily="Segoe UI Emoji"))

if __name__ == '__main__':
    # Dados
    a = np.array([15300, 16100, 17800, 16400]) # km
    e = np.array([.41, .342, .235, .3725])
    w = np.array([60, 10, 30, 60]) # deg
    i = np.array([30, 30, 0, 20]) # deg
    o = np.array([0, 40, 40, 40]) # deg
    tp = np.array([4708.5603, 5082.6453, 5908.5511, 5225.3666])
    TOA = np.array([60000] * 4)
    TOT = np.array([13581.1080927 , 19719.32768037, 11757.73393255, 20172.46081236])
    
    # Exercício 1
    satPos = []
    for k in range(4):
        pos = posVec(tp[k], a[k], e[k], w[k], i[k], o[k])
        satPos.append(pos)
    satPos = np.array(satPos).reshape([4, 3])

 
    # Plot Sat Position
    ax = plt.figure().add_subplot(projection='3d')
    plot1()
    plt.show()
    
    # Exercício 2
    TOF = TOA - TOT
    rho = TOF*C/1000
    
    # Função que faz o gradiente de forma automática
    # x = gradient_descent(grad, x0, Nsteps=200)
    
    # Abaixo rodo o gradiente de forma manual para plotar
    
    # Parâmetros
    Nsteps=200
    learningRate=0.6
    momentum=0.7
    x0 = np.array([[0, 0, 0]], dtype='float64')
    
    # Inicialização
    x = x0
    vel = np.array([[0, 0, 0]], dtype='float64')
    
    # Plot
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot1()
    ax.set_xlim([-7e3, -6e3])
    ax.set_ylim([-7e3, -6e3])
    ax.set_zlim([6e3, 7e3])
    
    colors = plt.cm.viridis(np.linspace(0, 1, Nsteps))
    positions = []
    
    for step in range(Nsteps):
        g = grad(x)
        vel = momentum * vel - learningRate * g
        x += vel
        
        if step % 4 == 0:
            positions.append(x.copy())
            ax.clear()
            plot1()
            ax.set_xlim([-7e3, -6e3])
            ax.set_ylim([-7e3, -6e3])
            ax.set_zlim([6e3, 7e3])
            for i, pos in enumerate(positions):
                alpha = 0.1 + 0.9 * (i / (len(positions) - 1)) if len(positions) > 1 else 1.0
                ax.scatter(pos[0][0], pos[0][1], pos[0][2], color=colors[i], alpha=alpha)

            plt.pause(0.2)

    print(x)
    plt.ioff()
    plt.show()
