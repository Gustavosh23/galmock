#!/usr/bin/env python
# coding: utf-8

# In[13]:


#Bibliotecas necessárias
import configparser
import h5py
import numpy as np
import pynbody
import pynbody.plot.sph as sph
import matplotlib.pyplot as plt
from sys import argv

'''
galmock.py

This python program adapts hdf5 snapshots of n-body simulations of isolated galaxies that use star formation, such as those from GADGET-4, allowing the plotting of realistic visualizations that take into account metallicity and particle age of the simulated galaxy.

Usage:
python3 galmock.py [snapshot --hdf5]
'''

########################################################################
# cria o objeto ConfigParser
config = configparser.ConfigParser()

# lê o arquivo .ini
config.read('param.ini')

# obtém os valores da seção "plot"
width = config.get('plot', 'width')
resolution = config.getint('plot', 'resolution')
starsize = config.getfloat('plot', 'starsize')
galrot = config.getint('plot', 'galrot')

# obtém os valores da seção "filters"
r_scale = config.getfloat('filters', 'r_scale')
g_scale = config.getfloat('filters', 'g_scale')
b_scale = config.getfloat('filters', 'b_scale')
dynamic_range = config.getfloat('filters', 'dynamic_range')
                                
# obtém os valores da seção "disk"
diskp = config.get('disk', 'diskp')
metaldisk = config.getfloat('disk', 'metaldisk')
min_metaldisk = config.get('disk', 'min_metaldisk')
########################################################################

# Define ordem do argumento ao iniciar o programa, no caso o argumento é o nome do seu snapshot a ser lido
snapshotIn = str(argv[1])

#Atribuindo o  do argumento 1 para o título do snapshot escolhido para ser lido pelo h5py
s = h5py.File(snapshotIn, "r")

#lendo as partículas tipo stars do arquivo hdf5
s_star = s['PartType4']

#importando partículas tipo disk caso existam
if 'PartType2' in h5py.File(snapshotIn, "r"):
    s_disk = s['PartType2']

#importando tempo do snapshot
s_time = s['Header'].attrs['Time']

#importando informações das partículas tipo stars
star_x = np.array(s_star['Coordinates'][:,0])
star_y = np.array(s_star['Coordinates'][:,1])
star_z = np.array(s_star['Coordinates'][:,2])
star_mass = np.array(s_star['Masses'])
star_metal = np.array(s_star['Metallicity'])
star_age = np.array(s_star['StellarFormationTime'])

#obtendo valores mínimos da idade e metalicidade das partículas stars
star_min_met = np.min(star_metal)
star_min_age = np.min(star_age)

#importando informações das partículas tipo disco caso existam
if 'PartType2' in h5py.File(snapshotIn, "r"): 
    disk_x = np.array(s_disk['Coordinates'][:,0])
    disk_y = np.array(s_disk['Coordinates'][:,1])
    disk_z = np.array(s_disk['Coordinates'][:,2])
    disk_mass = np.array(s_disk['Masses'])
    disk_metal = np.array(s_disk['Metallicity'])
    #atribuindo um valor de metalicidade para o disco de acordo com a escolha da variavel min)metaldisk do arquivo param.ini
    if min_metaldisk == 'True':
        for i in range(len(disk_metal)):
            disk_metal[i] += star_min_met
    else:
        for i in range(len(disk_metal)):
            disk_metal[i] += metaldisk
    
    disk_age = np.array(s_disk['StellarFormationTime'])
    for i in range(len(disk_age)):
        disk_age[i] += star_min_age

    

#decisão se há concatenação das partículsa tipo disco e stars ou se será considerado apenas estrelas de acordo com a escolha no arquivo param.ini    
if diskp == 'False':
    x = star_x
    y = star_y
    z = star_z
    mass = star_mass
    metal = star_metal
    age = star_age
else:
    x = np.concatenate((disk_x, star_x), axis=0)
    y = np.concatenate((disk_y, star_y), axis=0)
    z = np.concatenate((disk_z, star_z), axis=0)
    mass = np.concatenate((disk_mass, star_mass), axis=0)
    metal = np.concatenate((disk_metal, star_metal), axis=0)
    age = np.concatenate((disk_age, star_age), axis=0)

#correção de centro de massa do snapshot
com_x = np.sum(x*mass)/np.sum(mass)
com_y = np.sum(y*mass)/np.sum(mass)
com_z = np.sum(z*mass)/np.sum(mass)

x = (x - com_x)
y = (y - com_y)
z = (z - com_z)


#atribuindo Sim.Arrays para o pynobdy
Nstars = len(mass)
p = pynbody.snapshot.new(star=int(Nstars))
p.star['pos'] = pynbody.array.SimArray(np.empty((Nstars, 3)), units="kpc")
p.star['mass'] = pynbody.array.SimArray(np.empty((Nstars)), units="1.00e+10 Msol")
p.star['metals'] = pynbody.array.SimArray(np.empty((Nstars)), units=None)
p.star['age'] = pynbody.array.SimArray(np.empty((Nstars)), units="Gyr")

p.star['pos'][:,0] = x
p.star['pos'][:,1] = y
p.star['pos'][:,2] = z
p.star['mass'] = mass
p.star['metals'] = metal
p.star['age'] = s_time - age #pequena correção do tempo das partículas para formato esperado pela função do pynbody
p.stars.rotate_x(galrot)

#plotagem
pynbody.plot.stars.render(p, width=width, resolution=resolution, starsize=starsize, r_scale=r_scale, g_scale=g_scale, b_scale=b_scale, dynamic_range=dynamic_range, plot=True)

#salvando arquivo com a imagem gerada e dando nome de acordo com o tempo do snapshot
plt.savefig('galmock_'+str("%.2f"%s_time)+'.png', bbox_inches='tight', facecolor='white', dpi=300)


# In[ ]:




