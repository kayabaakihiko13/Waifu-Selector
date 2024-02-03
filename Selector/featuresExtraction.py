import cv2
import numpy as np
import matplotlib.pyplot as plt
import pywt

def dwt2d(img:np.ndarray, mode='haar',
          level:int|float=1) ->np.ndarray:
    """
    Discrete Wavelet Transform is particularly well-suited for
    capturing both frequency and location information in a signal or a image.
    it decomposes a signal into a set of wavelet functions at different scales
    and positions.
    Args:
        img (np.ndarray): _description_
        mode (str, optional): _description_. Defaults to 'haar'.
        level (int | float, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """
    imArray = img
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H

def _distance(points1,points2):
    return np.sqrt((points1[0]-points2[0])**2 +(points1[1] -points2[1])**2)

def gaussianHP(image:np.ndarray,cuttoff_freq:float):
    """
    Apply Gaussian High Pass Filter to an image using FFT
    Args:
        image (np.ndarray): input image (3-channel color image)
        cuttoff_freq (float): Cutoff frequency for the high pass filter.
    Returns:
        np.ndarray: Image with high pass filtering applied.
    """
    # convert image to monocrom
    if len(image.shape) == 3:
        imarray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # apply fft
    fft_image = np.fft.fft2(imarray)
    fft_shifted = np.fft.fftshift(fft_image)
    
    # generated Gaussian High Pass Filter
    rows , cols = imarray.shape
    crow,ccol = rows //2,cols // 2
    mask = np.ones((rows,cols),np.uint8)
    r = (cuttoff_freq * rows) // 2
    center = [crow,ccol]
    x, y = np.ogrid[:rows,:cols]
    masked_area = (x - center[0])**2 + (y-center[1]) ** 2 <= r*r
    mask[masked_area] = 0
    fft_shifted *=mask
    result_image = np.fft.ifft2(np.fft.ifftshift(fft_shifted)).real
    result_image = np.abs(result_image)
    return result_image.astype(np.uint8)

def FFT2D(image:np.ndarray):
    """
    Fast Fourier 2D is a highly optimized implemantation
    the discrete Fourier transform (DFT)
    Args:
        image (np.ndarray): input image array
    """
    # convert image to monocrom
    if len(image.shape) == 3:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image_transform = np.fft.fft2(image)
    magnitude_spectrum = np.fft.fftshift(np.log(np.abs(image_transform)+1))
    
    return magnitude_spectrum
