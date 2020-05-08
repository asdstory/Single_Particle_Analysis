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

# Output transformed image
plt.imsave('FFT.png',img_FFT)

# Method 2: Using OpenCV

https://medium.com/@hicraigchen/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82
