
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


# In[16]:


def walk_dataset (root):
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
                    print ((midi_data.instruments[0]))
                except:
                    counterr = counterr + 1
                    print (counterr)
                    pass
#                 midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
#                 d = parse_midi (d,c,midi_data)
                if (count==10):
                    return;


# In[17]:


root = "/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/DataSetTest"
walk_dataset(root)


# In[18]:


print (midi_data.instruments)


# In[26]:


pm = pretty_midi.PrettyMIDI()
instrument = midi_data.instruments[0]
pm.instruments.append(instrument)
instrument = midi_data.instruments[1]
pm.instruments.append(instrument)
pm.write("/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/output_1.mid")


# In[27]:


instrument.program

