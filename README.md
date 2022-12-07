#pygame virtual keyboard which assigns a prime number, light frequency, and sound frequency
#to keys. it mixes the light frequencies to corresponding RGB colors, mixes
#the pure tones to sounds, and multiplies the primes to get unique numbers.

This code assigns a color and sound to a range of positive integers in a natural
way.

Input: n

1) Factor n into a product of primes n = p_1^s_1 * ... * p_r ^s_r

2) Map every prime to a wavelength into the visible range which is roughly 380nm (800Thz, violet) - 700nm (400Thz, red). Use f_red*(f_violet/f_red)^((i-1)/(num_keys-1)) in analogy to the keyboard mapping of sound frequencies 440Hz*2^((i-49)/12).

3) For example, the number 197 is p_45. Its light frequency is 492 THz ->  608nm wavelength, so red. 563 is p_103, so 649 THz -> 462nm, so blue. Combining them we get the number 110911 which has a bright purple color. 

4) To convert this spectrum to the appropriate color of light we use the CIE color matching functions (https://www.cs.rit.edu/~ncs/color/t_spectr.html). This can be implemented in almost any language. (https://mathematica.stackexchange.com/questions/57389/convert-spectral-distribution-to-rgb-color/57457#57457).

Output: An RBG color specification.

A similar method can be used for sound, in which case we just scale into the audible range of 20Hz - 20kHz. We then need to mix the tones to get a sound using a synthesizer package, in this case tones.

Importantly, *spectra* of colors and sounds combine additively. Combining natural numbers via multiplication is straightforward.

This could be used to make a *keyboard whose keys are appropriately colored and labeled by prime numbers.
