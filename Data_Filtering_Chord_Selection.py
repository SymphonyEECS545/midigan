
# coding: utf-8

# In[1]:


import numpy as np
import pretty_midi
import sys
import os
import pandas as pd


# In[2]:


chords_major = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chords_minor = ['A1', 'A#1', 'B1', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1']
chord_map = {
    'C': ['C4', 'E4', 'G4'],
    'C#': ['C#4', 'F4', 'G#4'], 
    'D': ['D4', 'F#4', 'A4'], 
    'D#': ['D#4', 'G4', 'A#4'], 
    'E': ['E4', 'G#4', 'B4'],
    'F': ['F4', 'A4', 'C4'],
    'F#': ['F#4', 'A#4', 'C#4'], 
    'G': ['G4', 'B4', 'D4'],
    'G#': ['G#4', 'C4', 'D#4'], 
    'A': ['A4', 'C#4', 'E4'], 
    'A#': ['A#4', 'D4', 'F4'], 
    'B': ['B4', 'D#4', 'F#4'],
    'A1': ['A4', 'C4', 'E4'], 
    'A#1': ['A#4', 'C#4', 'E#4'],
    'B1': ['B4', 'D4', 'F#4'],
    'C1': ['C4', 'D#4', 'G4'],
    'C#1': ['C#4', 'E4', 'G#4'],
    'D1': ['D4', 'F4', 'A4'],
    'D#1': ['D#4', 'F#4', 'A#4'], 
    'E1': ['E4', 'G4', 'B4'],
    'F1': ['F4', 'G#4', 'C4'],
    'F#1': ['F#4', 'A4', 'C#4'],
    'G1': ['G4', 'A#4', 'D4'],
    'G#1': ['G#4', 'B4', 'D4']
}


# In[3]:


C = np.zeros((24,128))
c = 0
for i in chords_major:
    for j in chord_map[i]:
        C[c,pretty_midi.note_name_to_number(j)]=1
    c = c+1


# In[4]:


def piano_roll_to_pretty_midi(piano_roll, sf=16, program_num=1):
    """Convert piano roll to a single instrument pretty_midi object"""
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program_num)
 
    #prepend,append zeros so we can acknowledge inital and ending events
    piano_roll = np.hstack((np.zeros((notes, 1)),
                                 piano_roll,
                                 np.zeros((notes, 1))))
 
    velocity_changes = np.nonzero(np.diff(piano_roll).T)
    current_velocities = np.zeros(notes,dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        velocity = piano_roll[note, time + 1]
        time = time / sf
        if velocity > 0:
            if current_velocities[note] == 0:
                #print('note {} on'.format(pretty_midi.note_number_to_name(note)))
                #print('starting at time {} with velocity {}'.format(time,velocity))
                note_on_time[note] = time
                current_velocities[note] = velocity
            elif current_velocities[note] > 0:
                #change velocity with a special MIDI message
                pass
        else:
            #print('note {} off'.format(pretty_midi.note_number_to_name(note)))
            #print('ending at time {}'.format(time))
            pm_note = pretty_midi.Note(
            velocity=current_velocities[note],
            pitch=note,
            start=note_on_time[note],
            end=time)
            instrument.notes.append(pm_note)
            current_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm


# In[5]:


def shift_notes (piano_roll):
    """Shifts all notes into two octaves from C4 to B5"""
    r, c = np.shape(piano_roll)
    i=0
    piano_superimpose = np.zeros((16,c))
    while (i < 128):
        piano_superimpose = piano_superimpose + piano_roll[i:i+16,:]
        i = i + 16
    new_piano_roll = np.concatenate((np.zeros((72,c)), piano_superimpose, np.zeros((40,c))))
    return new_piano_roll


# In[6]:


def filter_chords (piano_roll):
    """Filter out the 12 basic chord triads"""
    chords_present = np.dot(C,piano_roll)
    chords_selected = np.where((chords_present>0) & (chords_present==np.amax(chords_present,axis=0)),1,0)
    chords_filtered = np.dot(np.transpose(C),chords_selected)
    return chords_filtered


# In[7]:


def parse_instruments (a, target_filename):
    idx = -1
    melody_idx = -1
    chord_idx = -1
    count_melody1 = 0
    count_chord1 = 0
    for inst in a.instruments:
        idx = idx + 1
        piano_roll = shift_notes(inst.get_piano_roll(16))
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
        prm = shift_notes(instrument.get_piano_roll(16))
        pmm = piano_roll_to_pretty_midi(prm,16,1)
        pm.instruments.append(pmm.instruments[0])
        
        instrument = a.instruments[chord_idx]
        prc = filter_chords(instrument.get_piano_roll(16))
        pmc = piano_roll_to_pretty_midi(prc,16,26)
        pm.instruments.append(pmc.instruments[0])
        pm.write("/Users/sbnahata/Documents/University of Michigan/EECS 545/Training Stage 1/" + target_filename)
        return 1
    else:
        return 0


# In[12]:


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
            if (count==1000 or counterr==500):
                return;


# In[ ]:


root = "/Users/sbnahata/Documents/University of Michigan/EECS 545/DataSetTest"
walk_dataset(root)


# In[ ]:


instrument = midi_data.instruments[0]
piano_roll = instrument.get_piano_roll(16)


# In[ ]:


npr = shift_notes(piano_roll)


# In[ ]:


pm = piano_roll_to_pretty_midi(npr,16,1)


# In[ ]:


pm.write("/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/S8.mid")


# In[ ]:


instrument = midi_data.instruments[3]
piano_roll = instrument.get_piano_roll(16)


# In[ ]:


pm3 = piano_roll_to_pretty_midi(filter_chords(piano_roll),16,27)


# In[ ]:


pm3.write("/Users/sbnahata/Documents/University of Michigan/EECS 545/Project/S16Chords.mid")


# In[ ]:


parse_instruments(midi_data,"STest.mid")

