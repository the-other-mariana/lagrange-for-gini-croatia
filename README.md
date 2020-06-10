# Lagrange Interpolation Method for Lorenz Curve Approximation

This project consists of a program that calculates the Gini coefficient in the case of Croatia 2018. For the gini calculation, the program first reads from a csv file containing the income distribution by tenths of population. Then, creates the coordinates needed to plot Lorenz curve. The actual Lorenz curve is calculated as a polynomial using Lagrange Interpolation Method with calculated points. The program then calculates the gini coefficient by integrating x minus the lorenz function.

## Specifications

Python version: `Python 3.6.2`
Matplotlib version: `2.1.2`
Sympy version: `1.5.1`
Numpy version: `1.14.1`

## Usage

Download this folder and store it in your computer.
Run `lagrange.py` by typing `python lagrange.py` once located in the project's folder. 