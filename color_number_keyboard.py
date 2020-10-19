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
import sys
import numpy as np
import math
import sympy
from sympy.ntheory import factorint
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import winsound

num_keys = 88 #number of keys on keyboard
prime_index = {sympy.prime(i):i for i in range(1,num_keys+1)} #index of primes

#constants for light
c=299792458 #speed of light in m/s
lambda_violet = np.float64(380*10**-9) #wavelength of violet light, ~380nm
lambda_red = np.float64(750*10**-9) #wavelength of red light, ~750nm
f_red = c/lambda_red #freq. of red light, ~400THz
f_violet = c/lambda_violet #freq of violet light, ~788Thz
L = 100 #scaling factor controlling brightness/luminosity

#constants for sound
f_C = 440 #frequency of C note in Hz
b_sound = np.power(2,1/12)

#import RGB values from CIE 1931 color specification
#http://www.cvrl.org/database/data/cmfs/ciexyzjv.csv
#first column is wavelengths in nm as ints in steps of 5
#next 3 columns are x,y,z tristimulus values as floats
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

#interpolate x, y, z color data to smooth color functions
x_bar = interp1d(wavelengths, x)
y_bar = interp1d(wavelengths, y)
z_bar = interp1d(wavelengths, z)

#assign each prime number a frequency in visible spectrum
def light_freq(prime):
    i=prime_index[prime]
    return np.power(f_violet/f_red,(i-1)/(num_keys-1))*f_red

#assign each prime number a frequency in audible spectrum
def sound_freq(prime):
    i=prime_index[prime]
    return np.power(b_sound,i-49)*f_C

#factor integer to obtain prime factorization
#assign delta functions centered at each prime in factorization
#multiplicity of prime scales corresponding delta function
#perform convolution (integral against color matching function) to obtain XYZ
#integral of delta function is just *value* of color matching function
#results in weighted sum over primes present
def XYZ(n):
    fact = factorint(n)
    X = sum([mult*x_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    Y = sum([mult*y_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    Z = sum([mult*z_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    return L*np.array([X,Y,Z])

#define constant RGBtoXYZ transformation matrix
XYZtoRGB=(1/.17697)*np.array([[.49000,.31000,.20000],[.17697,.81240,.01063],[.00000,.01000,.99000]])
#convert XYZ tristimulus values to RGB colors using matrix
def sRGB(XYZ):
    RGB = np.matmul(np.linalg.inv(XYZtoRGB),XYZ)
    return np.array(list(map(gamma,RGB)))

#non-linear gamma correction to transform RGB to sRGB
def gamma(u):
    if u <= .0031308:
        return (323/25)*u
    else:
        return (211*math.pow(u,5/12)-11)/200

if __name__ == "__main__":
    keys = input("Enter set of keys:").split(",") #input multi-set of keys
    keys=list(map(int,keys)) #convert strings to ints
    keys=list(map(sympy.prime,keys)) #map key number to primes
    #compute number, color, sound for input
    n=math.prod(keys) #multiply primes together
    color=sRGB(XYZ(n)) #get RGB color associated to n
    sound=list(map(sound_freq,keys)) #get sound frequencies associated to keys
    #output number, color, sound to terminal
    sys.stderr.write("Number: "+str(n)+"\n")
    sys.stderr.write("RGB Color: "+str(color)+"\n")
    sys.stderr.write("Sound: "+str(sound)+"\n")
    #output sound via speaker, color and number via display
    if 37 <= sound[0] <= 32767:
        winsound.Beep(math.floor(sound[0]),1000) #can only play single tone for now
    plt.title(str(n))
    plt.imshow([[color]])
    plt.show()
