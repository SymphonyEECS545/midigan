
# coding: utf-8

# In[6]:


import numpy as np
import pretty_midi
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


# In[7]:


get_ipython().magic('matplotlib inline')

plt.rcParams['axes.labelsize'] = 20
plt.rcParams['axes.titlesize']=30
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


# In[20]:


def walk_dataset (root, d):
    count = 0
    counterr = 0
    for path, subdirs, files in os.walk(root):
        for midifile in files:
            if midifile.startswith('.') or not midifile.endswith('.mid'):
                continue
            else:  
                count = count + 1
                print (str(count) + ' ' + os.path.join(path, midifile))
                try:
                    midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
                    parse_midi(d, midi_data)
                except:
                    counterr = counterr + 1
                    print (counterr)
                    pass
#                 midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
#                 d = parse_midi (d,c,midi_data)
#                 midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
#                 parse_midi(d, midi_data)
                if (count==100):
                    return d;


# In[21]:


def parse_midi (occurences, midi_data):
    for inst in midi_data.instruments:
        if (inst.program in occurences.keys()):
            occurences[inst.program] = occurences[inst.program] + 1
        else:
            occurences[inst.program] = 1
    return occurences


# In[22]:


d={}
root = "/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/DataSetTest"
walk_dataset(root, d)

