#maps numbers to frequencies in an multiplicative-to-addtitive manner
#interprets sound as formed from "pure tones" at each frequency
#interprets color as formed from "pure light" at each frequency
#sets up a keyboard in which each key represents a color, number, and tone
#
#keyboard maps each key (integer)
#to an RGB color (or non-visible), an audible frequency (or in-audible),
#and an integer
#
#programmatically, there are 3 separate dictionaries for sound, color, and
#number. the final keyboard will take any subset of integers as input
#and provide the mixing as output
################################################################################
################################################################################

import csv
import numpy as np
import math
from sympy.ntheory import factorint
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

c=299792458 #speed of light in m/s
lambda_violet = 380*10**-9 #wavelength of violet light, ~380nm
lambda_red = 750*10**-9 #wavelength of red light, ~750nm
f_red = c/lambda_red #freq. of red light, ~400THz
f_violet = c/lambda_violet #freq of violet light, ~788Thz

L = 680 #parameter controlling brightness/luminosity
f_0 = f_red #set initial freqency to correspond to red
base = 17 #set the base of the logarithm

#import RGB values from CIE 1931 color specification
#http://www.cvrl.org/database/data/cmfs/ciexyzjv.csv
#first column is wavelengths in nm as ints in steps of 5
#next 3 columns are x,y,z values as floats
cie_data=dict()
with open('ciexyzjv.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        cie_data[int(row[0])] = list(map(float,row[1:]))

#get array of wavelengths (converted to meters) and x, y, z color data
wavelengths = (10**-9)*np.array(list(cie_data.keys()))
color_data = np.array(list(cie_data.values()))
x = color_data.T[0]
y = color_data.T[1]
z = color_data.T[2]

#plot x, y, z color data
#plt.plot(wavelengths,x)
#plt.plot(wavelengths,y)
#plt.plot(wavelengths,z)
#plt.show()

#interpolate x, y, z color data to smooth color functions
x_bar = interp1d(wavelengths, x)
y_bar = interp1d(wavelengths, y)
z_bar = interp1d(wavelengths, z)

#define frequency of prime number as
def freq(base,prime):
    return f_0*math.log(prime,base)

#factor integer to obtain prime factorization
#assign delta functions centered at each prime in factorization
#multiplicity of prime scales corresponding delta function
#perform convolution (integral against color matching function) to obtain XYZ
#integral of delta function is just *value* of color matching function
#results in weighted sum over primes present
def XYZ(n):
    fact = factorint(n)
    X = L*sum([mult*x_bar(c/freq(base,prime)) for prime,mult in fact.items()])
    Y = L*sum([mult*y_bar(c/freq(base,prime)) for prime,mult in fact.items()])
    Z = L*sum([mult*z_bar(c/freq(base,prime)) for prime,mult in fact.items()])
    return [X,Y,Z]
