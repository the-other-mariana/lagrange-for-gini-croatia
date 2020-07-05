import sympy
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sympy.plotting.plot import List2DSeries
from timeit import default_timer as timer
import random


matplotlib.style.use('bmh')
#seaborn-whitegrid
#fivethirtyeight

def Lagrange (Lx, Ly):
    X = sympy.symbols('X')
    if  len(Lx) != len(Ly):
        print ("Error data set")
        return 1
    y = 0
    for i in range(len(Lx)):
        t = 1
        for j in range(len(Lx)):
            if j != i:
                t *= ((X - Lx[j]) / (Lx[i] - Lx[j]))
        y += t * Ly[i]
    return y

GINI_KNOWN = 0.293 # here is Croatia's gini in 2018
Lx = []
Ly = []
yPos = []

Ly.append(0.0)
with open('input_hrv.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        r = 0
        for value in row:
            r += 1
            try:
                value = float(value)
                if r % 2 == 0:
                    Ly.append(value)
            except ValueError as e:
                continue
GDP = Ly[-1]
del Ly[-1]
Ly.sort()
for i in range(len(Ly)):
    Lx.append(i * 10.0)

print("---------- Dependencies ----------")
print('matplotlib: {}'.format(matplotlib.__version__))
print('sympy: {}'.format(sympy.__version__))
print('numpy: {}'.format(np.__version__))
print("----------------------------------")

print("----------- INPUT DATA -----------")
print("X Data: ", Lx)
print("Y Data: ", Ly)
print("Total Income: ", GDP)
print("----------------------------------")

print("----------- SET POINTS -----------")
for i in range(len(Lx)):
    yValue = (Ly[i] * 1.0) / (GDP * 1.0) * 100.0
    if i != 0:
        yValue += yPos[i - 1]
    print("X: ", Lx[i], "Y: ", yValue)
    yPos.append(yValue)
print("----------------------------------")

print("----------- INPUT DATA ------------")
print("X Vector: ", Lx)
print("Y Vector: ", yPos)
print("-----------------------------------")

X = sympy.symbols('X')
xLimit = 100

startL = timer()
MyLagrange = Lagrange(Lx, yPos)
lorenz = sympy.simplify(MyLagrange)
equality = X
areaEquality = sympy.integrate(equality, (sympy.Symbol('X'), 0, xLimit))
areaGINI = sympy.integrate(equality - lorenz, (sympy.Symbol('X'), 0, xLimit))
lagGINI = areaGINI / areaEquality
endL = timer()

timeLagrange = endL - startL
lagAccuracy = abs(100.0 - (abs(GINI_KNOWN - lagGINI) / GINI_KNOWN) * 100.0)

print("------------ LAGRANGE ------------")
print("Lagrange Polynomial:", lorenz)
print("Object Type:", type(lorenz))
print("Enclosed Area:", areaGINI)
print("Equality Area:", areaEquality)
print("GINI Coefficient:", lagGINI)
print("Time:", timeLagrange, "seconds")
print("Accuracy: {:0.2f} %".format(lagAccuracy))
print("----------------------------------")

print("+++++++++++++ INTEGRATION ++++++++++++")
delta = 0.005
acc = 0.0
accArea = 0.0
eqArea = 0.0

startR = timer()
while acc <= xLimit:
    acc += delta
    eval = acc - (delta / 2.0)
    heightEq = equality.evalf(subs={X:eval})
    heightLorenz = lorenz.evalf(subs={X:eval})
    eqArea += delta * (heightEq)
    accArea += delta * (heightEq - heightLorenz)
endR = timer()
timeRiemann = endR - startR
rieGINI = accArea / eqArea
rieAccuracy = abs(100.0 - (abs(GINI_KNOWN - rieGINI) / GINI_KNOWN) * 100.0)

print("------------ RIEMANN ------------")
print("Enclosed Area:", accArea)
print("Equality Area:", eqArea)
print("GINI Coefficient:", rieGINI)
print("Time:", timeRiemann, "seconds")
print("Accuracy: {:0.2f} %".format(rieAccuracy))
print("----------------------------------")

tests = 50000
inside = 0.0
areaDomain = 100 * 100
insidePoints = []

startMC = timer()
for i in range(tests):
    xCoord = random.uniform(0, 100)
    yCoord = random.uniform(0, 100)

    if yCoord <= equality.evalf(subs={X:xCoord}) and yCoord >= lorenz.evalf(subs={X:xCoord}):
        inside += 1.0
        point = [xCoord, yCoord]
        insidePoints.append(point)
endMC = timer()

timeMC = endMC - startMC
MonteCarloArea = (inside / tests) * areaDomain
mcGINI = MonteCarloArea / areaEquality
mcAccuracy = abs(100.0 - (abs(GINI_KNOWN - mcGINI) / GINI_KNOWN) * 100.0)
print("------------ MONTE CARLO ------------")
print("Enclosed Area:", MonteCarloArea)
print("GINI Coefficient:", mcGINI)
print("Time:", timeMC, "seconds")
print("Accuracy: {:0.2f} %".format(mcAccuracy))
print("------------------------------------")

# Plots
p1 = sympy.plotting.plot(lorenz, equality, (X, 0, xLimit), ylim=[0,100],show=False)
p1.title = "Lagrange Interpolation for GINI Approximation"
p1[0].line_color='r'

p2 = sympy.plotting.plot(lorenz, equality, (X, 0, xLimit), ylim=[0,100],show=False)
p2.title = "Lagrange Interpolation vs. Data Set Comparison"
p2.append(List2DSeries(Lx, yPos))
p2[2].line_color=(0.5, 0.5, 0.5)
p2[0].line_color='r'


# Time Performance visualization
finalTime = [timeLagrange, timeMC, timeRiemann]
labels = ["Python", "Monte Carlo", "Riemann"]
index = np.arange(len(labels))
viridis = matplotlib.cm.get_cmap('viridis', 5)
bars = plt.bar(index, finalTime, color=viridis.colors[2])
plt.xlabel('Method for Polynomial Integration', fontsize=13)
plt.ylabel('Time (s)', fontsize=13)
plt.xticks(index, labels, fontsize=8, rotation=0)
plt.title('Time Performance Comparison')

'''
# For Monte Carlo visualization

xx = np.linspace(0, 100, 1000)
yy = sympy.lambdify(X, [equality, lorenz])(xx)
plt.plot(xx, np.transpose(yy))
for i in range(len(insidePoints)):
    plt.plot(insidePoints[i][0], insidePoints[i][1], color='red', marker='o')
'''
'''
# For Riemann visualization
xx = np.linspace(0, 100, 1000)
yy = sympy.lambdify(X, [equality, lorenz])(xx)
plt.plot(xx, np.transpose(yy))

f = sympy.lambdify(X, lorenz)
a = 0; b = 100; N = 10
n = 10
x = np.linspace(a,b,N+1)
y = f(x)
x_mid = (x[:-1] + x[1:])/2 # midpoints
y_mid = f(x_mid)
plt.bar(x_mid,y_mid,width=(b-a)/N,alpha=0.2,edgecolor='b')
plt.title('Midpoint Riemann Sum, N = {}'.format(N))
'''

p1.show()
p2.show()
plt.show()
