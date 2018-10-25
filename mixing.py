#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Created on Sep 2018
    
    @author: BH @ BNU
    '''

#from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#from pylab import *

#number of pixel
n_sides = 512
#field degree (have to be a squared field)
field_deg = 3.41
#lensing amplitude magnification factor
magnif = 1.5e-5

#import data
cmb_map_data_path = './map_data.dat'
cmb_map_data = np.loadtxt(cmb_map_data_path)
#print(cmb_map_data.shape)
#plt.imshow(cmb_map_data)

lens_map_data_path = './lens_data.dat'
lens_map_data = np.loadtxt(lens_map_data_path)
#magnify lens map by a facotor
lens_map_data = magnif*lens_map_data
#print(lens_map_data.shape)
#plt.imshow(lens_map_data)

#step-size of derivative
h = field_deg/n_sides

#lensed cmb map
lensed_cmb_map_data = np.zeros(shape=(n_sides,n_sides),dtype='float')

for i in range (0,n_sides):
    for j in range (0,n_sides):
        #compute the deflection field: x-component
        if(i==0):
            partial_x_psi = (lens_map_data[i+1,j]-lens_map_data[i,j])/h
        elif(i==(n_sides-1)):
            partial_x_psi = (lens_map_data[i,j]-lens_map_data[i-1,j])/h
        else:
            partial_x_psi = (lens_map_data[i+1,j]-lens_map_data[i-1,j])/2.0/h
        #compute the deflection field: y-component
        if(j==0):
            partial_y_psi = (lens_map_data[i,j+1]-lens_map_data[i,j])/h
        elif(j==(n_sides-1)):
            partial_y_psi = (lens_map_data[i,j]-lens_map_data[i,j-1])/h
        else:
            partial_y_psi = (lens_map_data[i,j+1]-lens_map_data[i,j-1])/2.0/h
        #get lensed coordinate
        old_x = h*i
        new_x = old_x + partial_x_psi
        old_y = h*j
        new_y = old_y + partial_y_psi
        #get the new coordinate index
        new_x_idx = int(new_x/h)
        new_y_idx = int(new_y/h)
        #cyclic boundary: lower bound
        if(new_x_idx<0):
            new_x_idx = n_sides+new_x_idx
        if(new_y_idx<0):
            new_y_idx = n_sides+new_y_idx
        #cyclic boundary: upper bound
        if(new_x_idx>(n_sides-1)):
            new_x_idx = new_x_idx-n_sides
        if(new_y_idx>(n_sides-1)):
            new_y_idx = new_y_idx-n_sides
        #moving pixel
        lensed_cmb_map_data[i,j] = cmb_map_data[new_x_idx,new_y_idx]


'''
for i in range (0,n_sides):
    for j in range (0,n_sides):
        #compute the spatial derivative along x-axis
        if(i==0):
            partial_x_psi = (lens_map_data[i+1,j]-lens_map_data[i,j])/h
            partial_x_cmb = (cmb_map_data[i+1,j]-cmb_map_data[i,j])/h
        elif(i==(n_sides-1)):
            partial_x_psi = (lens_map_data[i,j]-lens_map_data[i-1,j])/h
            partial_x_cmb = (cmb_map_data[i,j]-cmb_map_data[i-1,j])/h
        else:
            partial_x_psi = (lens_map_data[i+1,j]-lens_map_data[i-1,j])/2.0/h
            partial_x_cmb = (cmb_map_data[i+1,j]-cmb_map_data[i-1,j])/2.0/h
        #compute the spatial derivative along y-axis
        if(j==0):
            partial_y_psi = (lens_map_data[i,j+1]-lens_map_data[i,j])/h
            partial_y_cmb = (cmb_map_data[i,j+1]-cmb_map_data[i,j])/h
        elif(j==(n_sides-1)):
            partial_y_psi = (lens_map_data[i,j]-lens_map_data[i,j-1])/h
            partial_y_cmb = (cmb_map_data[i,j]-cmb_map_data[i,j-1])/h
        else:
            partial_y_psi = (lens_map_data[i,j+1]-lens_map_data[i,j-1])/2.0/h
            partial_y_cmb = (cmb_map_data[i,j+1]-cmb_map_data[i,j-1])/2.0/h
        #add the spatial gradient term to the primary cmb
        #lensed_cmb_map_data[i,j] = cmb_map_data[i,j] + partial_x_cmb*partial_x_psi + partial_y_cmb*partial_y_psi
'''

lensed_cmb_map_data = cmb_map_data + lens_map_data

plt.imshow(lensed_cmb_map_data,cmap='bwr',vmin=-1e-4,vmax=1e-4)

plt.axis('off')
plt.colorbar()
#plt.show()
plt.savefig('lensed_cmb_map.png')

exit()
