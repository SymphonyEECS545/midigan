
# coding: utf-8

# In[1]:


import numpy as np
import pretty_midi
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


get_ipython().magic('matplotlib inline')

plt.rcParams['axes.labelsize'] = 20
plt.rcParams['axes.titlesize']=30
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


# In[3]:


def parse_midi (energy, occurences, midi_data):
    notes = midi_data.get_piano_roll(fs=100, times = None)
    ins_list = pretty_midi.INSTRUMENT_MAP
    if not energy:
        for i in range(len(notes)):
            a = sum(notes[i])
            energy[ins_list[i]]=[a]
            if a>0:
                occurences[ins_list[i]]=[1]
            else:
                occurences[ins_list[i]]=[0]
    else:
        for i in range(len(notes)):
            a = sum(notes[i])
            energy[ins_list[i]].append(a)
            if a>0:
                occurences[ins_list[i]].append(1)
            else:
                occurences[ins_list[i]].append(0)
    return 


# In[ ]:


d={}
c={}

root = "/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/DataSetTest"
count = 0
for path, subdirs, files in os.walk(root):
    for midifile in files:
        if midifile.startswith('.') or not midifile.endswith('.mid'):
            continue
        else:  
            count = count + 1
            print (str(count) + ' ' + os.path.join(path, midifile))
            try:
                midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
                parse_midi (d,c,midi_data)
            except:
                pass


# In[ ]:


data_energy = pd.DataFrame.from_dict(d)
data_occurence = pd.DataFrame.from_dict(c)
data_occurence


# In[10]:


data_occurence.sum(axis=0).sort_values(ascending=False)

