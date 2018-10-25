#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Sep 2018
    
@author: BH @ BNU
'''

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

#lensing potential amplitude
lensing_amp = 1.0

#读取图片,灰度化，并转为数组
im = array(Image.open('./lens_image/ali_512.png').convert('L'),'f')

#输出数组的各维度长度以及类型
print(im.shape,im.dtype)

#rescaling the lensing potential
im_max = max(im.flatten())
im_min = min(im.flatten())
if(im_min == 0.0):
    im_min = 0.1

#print(im_max,im_min)
#quit()

h = im_max - im_min
b = (1.0/im_max+1.0/im_min)/(1.0/im_max-1.0/im_min)
a = (1.0-b)/im_max
im = lensing_amp * (a*im + b)

#saving lensing potential data
np.savetxt('lens_data.dat', im)

#plot lensing potential
lens_data_path = './lens_data.dat'
lens_data = np.loadtxt(lens_data_path)
plt.imshow(lens_data,cmap='binary')
#plt.show()
plt.axis('off')
plt.colorbar()
plt.savefig('lens_map.png')

exit()

