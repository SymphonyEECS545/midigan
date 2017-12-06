
# coding: utf-8

# In[1]:


import numpy as np
import pretty_midi
import sys
import os
import pandas as pd


# In[2]:


root = "/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/DataSetTest"


# In[3]:


def parse_instruments (a, target_filename):
    idx = -1
    melody_idx = -1
    chord_idx = -1
    count_melody1 = 0
    count_chord1 = 0
    for inst in a.instruments:
        idx = idx + 1
        piano_roll = inst.get_piano_roll(16)
        index = ['Row'+str(j) for j in range(1, len(piano_roll)+1)]
        df = pd.DataFrame(piano_roll, index=index)
        p = df.astype(bool).sum(axis=0)
        count_melody = p[p==1].sum()
        count_chord = p[p>=3].sum()
        if count_melody > count_melody1:
            melody_idx = idx
            count_melody1 = count_melody
        if count_chord > count_chord1:
            chord_idx = idx
            count_chord1 = count_chord
    if melody_idx >= 0 and chord_idx >= 0:
        pm = pretty_midi.PrettyMIDI()
        instrument = a.instruments[melody_idx]
        instrument.program = 1
        pm.instruments.append(instrument)
        instrument = a.instruments[chord_idx]
        instrument.program = 26
        pm.instruments.append(instrument)
        pm.write("/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/Training Data/" + target_filename)
        return 1
    else:
        return 0


# In[4]:


def walk_dataset (root):
    count = 0
    counterr = 0
    for path, subdirs, files in os.walk(root):
        for midifile in files:
            if midifile.startswith('.') or not midifile.endswith('.mid'):
                continue
            else:  
                try:
                    midi_data = pretty_midi.PrettyMIDI(os.path.join(path, midifile))
                    target_filename = "Test_" + midifile
                    count = count + parse_instruments(midi_data, target_filename)
                except:
                    counterr = counterr + 1
                    print("Failure number: ", counterr)
                    pass
            if (count%20 == 0):
                print("Number of test songs created: ", count)
            if (count==1000 or counterr==100):
                return;


# In[5]:


walk_dataset(root)

