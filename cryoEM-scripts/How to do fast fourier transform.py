# Python program to read  
# image using matplotlib 
  
# importing matplotlib modules 
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
  
# Read Images 
img = mpimg.imread('g4g.png') 

# Output Images 
plt.imshow(img) 
plt.imsave('test.png',img)

# Importing numpy modules
import numpy as np

# Do FFT for the image
img_FFT = np.fft.fft2(img)

# Center spectrum
center = np.fft.fftshift(img_FFT)

# Output transformed image
plt.imsave('FFT_center.png',center)

# Method 2: Using OpenCV

# https://medium.com/@hicraigchen/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
cv2.imread('FFT.jpg',magnitude_spectrum)

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

# Or simply: 

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('class_averages-2.jpg',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
cv2.imwrite('FFT.jpg',magnitude_spectrum)
