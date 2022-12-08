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

import sys, os, csv
import numpy as np
import math, sympy
from sympy.ntheory import factorint
from scipy.interpolate import interp1d
import pygame
from pygame.locals import *
from tones import SINE_WAVE
from tones.mixer import Mixer
import time

num_keys = 144 #number of keys on keyboard
prime_index = {sympy.prime(i):i for i in range(1,num_keys+1)} #index of primes

#constants for light
c=299792458 #speed of light in m/s
lambda_violet = np.float64(380*10**-9) #wavelength of violet light, ~380nm
lambda_red = np.float64(750*10**-9) #wavelength of red light, ~750nm
f_red = c/lambda_red #freq. of red light, ~400THz
f_violet = c/lambda_violet #freq of violet light, ~788Thz
L = 1 #scaling factor controlling brightness/luminosity

#constants for sound
f_C = 110.0 #frequency of C note in Hz
b_sound = np.power(2,1/12)

#import RGB values from CIE 1931 color specification
#http://www.cvrl.org/database/data/cmfs/ciexyzjv.csv
#first column is wavelengths in nm as ints in steps of 5
#next 3 columns are x,y,z tristimulus values as floats
cie_data=dict()
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir,"ciexyzjv.csv")
print(this_dir)
print(DATA_PATH)
with open(DATA_PATH, newline='') as csvfile:
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
def XYZ(nH):
    fact = factorint(n)
    X = sum([mult*x_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    Y = sum([mult*y_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    Z = sum([mult*z_bar(c/light_freq(prime)) for prime,mult in fact.items()])
    return L*np.array([X,Y,Z])

#define constant RGBtoXYZ transformation matrix
XYZtoRGB=np.array([[3.24096994,-1.53738318,-.49861076],[-.96924364,1.8759675,.04155506],[.05563008,-.20397696,1.05697151]])
#convert XYZ tristimulus values to RGB colors using matrix
def sRGB(XYZ):
    RGB = np.matmul(XYZtoRGB,XYZ)
    return np.array(list(map(gamma,RGB)))

#non-linear gamma correction to transform RGB to sRGB
def gamma(u):
    if u <= .0031308:
        g = (323/25)*u
    else:
        g = (211*math.pow(u,5/12)-11)/200
    if g < 0:
        return 0
    elif g > 1:
        return 1
    else:
        return g

#display function for pygame
def display(str,color):
    text = font.render(str, True, (0, 0, 0), color)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    print(color)
    screen.fill(color)
    screen.blit(text, textRect)
    pygame.display.update()

if __name__ == "__main__":
    #initialize the pygame display
    pygame.init()
    screen = pygame.display.set_mode( (640,480) )
    pygame.display.set_caption('Synesthesiaer')
    screen.fill((174, 182, 245))
    font = pygame.font.Font(None, 36)

    done = False
    while not done:
        #get input from keyboard
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        pressed=[i for i in range(len(keys)) if keys[i] == True]
        if len(pressed) > 0:
            primes_pressed=list(map(sympy.prime,pressed)) #map key number to primes
            #compute number, color, sound for input
            n=np.prod(primes_pressed) #multiply primes together
            rgb_color=sRGB(XYZ(n)) #get RGB color associated to n
            int_rgb_color = tuple([math.floor(255*value) for value in rgb_color])
            tones=list(map(sound_freq,primes_pressed)) #get sound frequencies associated to keys
            #play sound from frequencies
            if len(tones) > 0 and 37 <= tones[0] <= 32767:
                #mix the tones of the different frequencies
                mixer = Mixer(44100, 0.5) #Create mixer, set sample rate and amplitude
                for i in range(len(tones)):
                    mixer.create_track(i, SINE_WAVE, attack=0.01, decay=0.1) #Create monophonic track
                    mixer.add_tone(i, frequency=tones[i], duration=0.25, amplitude=1.0) #add tone at given frequency
                mixer.write_wav("tones.wav") #Mix all tracks into a single list of samples and write to .wav file
                samples = mixer.mix() #Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and return the sample list
                #play sound using pygame
                pygame.mixer.init()
                mixed_tones = pygame.mixer.Sound("tones.wav")
                mixed_tones.play()
            #display number and color associated to keys pressed
            print(tones,str(n),int_rgb_color)
            display(str(n),int_rgb_color)

        if keys[K_ESCAPE]:
            done = True
