# Lagrange Interpolation Method for Lorenz Curve Approximation

This project consists of a program that calculates the Gini coefficient in the case of Croatia 2018. For the gini calculation, the program first reads from a csv file containing the income distribution by tenths of population. Then, creates the coordinates needed to plot Lorenz curve. The actual Lorenz curve is calculated as a polynomial approximation using Lagrange Interpolation Method with calculated coordinates. The program then calculates the gini coefficient by integrating x minus the lorenz function. Two other methods are added to calculate gini coefficient, but only for comparison.

## Specifications

Python version: `Python 3.6.2`<br />
Matplotlib version: `2.1.2`<br />
Sympy version: `1.5.1`<br />
Numpy version: `1.14.1`

## Usage

Download this folder and store it in your computer.<br />
Run `lagrange.py` by typing `python lagrange.py` once located in the project's folder. 

## Results

![alt text](https://github.com/the-other-mariana/lagrange-for-gini-croatia/blob/master/results/lorenz-curve-hrv.png?raw=true)