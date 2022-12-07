#pygame virtual keyboard which assigns a prime number, light frequency, and sound frequency
#to keys. it mixes the light frequencies to corresponding RGB colors, mixes
#the pure tones to sounds, and multiplies the primes to get unique numbers.

This code assigns a color and sound to a range of positive integers in a natural
way.

Input: n

1) Factor n into a product of primes n = p_1^s_1 * ... * p_r ^s_r

The only added input is how we scale the wavelengths. The default implementation maps the wavelength of every prime smoothly into the visible range which is roughly 380nm (800Thz, violet) - 700nm (400Thz, red)

3) To convert this spectrum to the appropriate color of light we use the CIE color matching functions (https://www.cs.rit.edu/~ncs/color/t_spectr.html). This can be implemented in almost any language. (https://mathematica.stackexchange.com/questions/57389/convert-spectral-distribution-to-rgb-color/57457#57457).

Output: An RBG color specification.

A similar method can be used for sound, in which case we just scale into the audible range of 20Hz - 20kHz. We then need to mix the tones to get a sound using a synthesizer package, in this case tones.

Importantly, *spectra* of colors and sounds combine additively. Combining natural numbers via multiplication is straightforward.

This could be used to make a *keyboard whose keys are appropriately colored and labeled by prime numbers.
