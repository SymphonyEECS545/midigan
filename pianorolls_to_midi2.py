#!/usr/bin/env python
import numpy as np
import pretty_midi 


def GetNoteArray(pianoroll):
    #get shape of piano roll
    notes, frames = np.shape(pianoroll)

    maxnote=0
    for i in range(frames):
        col=pianoroll[:,i]
        if len(np.nonzero(col))>maxnote:
            maxnote=len(np.nonzero(col))
        
    #initialize output using max number of notes we see at once
    output=np.zeros((maxnote,frames))


    #set init to first column and get nonzero values
    init=pianoroll[:,0]
    prev=np.nonzero(init)[0]

    #set init values in output
    for idx,note in enumerate(prev):
        output[idx,0]=note


    i=1
    #print "prev = "+str(prev)
    while(i<frames):
        
        currcol=pianoroll[:,i] #current frame in pianoroll
        curr=np.nonzero(currcol)[0] #nonzero indices
        #print "curr = "+str(curr)
        for idx, prevnote in enumerate(prev):
            
            if prevnote in curr:
                #if prev note is found in current notes add it to same place in array
                #and remove it from list, otherwise skip it
                indexcurr = np.argwhere(curr==prevnote)
                #print 'index '+str(idx)+' with note '+str(prevnote)
                output[idx,i]=prevnote
                curr = np.delete(curr, indexcurr)
                
            else:
                continue
        #now cycle over notes that haven't been seen in prev
        for idx, currnote in enumerate(curr):
            j=0
            while j<maxnote:
                if output[j,i]==0:
                    output[j,i]=currnote
                    break
                else:
                    j=j+1
            
        
        #finally set prev col to what we just organized
        prev=output[:,i]
        #prev=np.nonzero(prevcol)[0]
        #print 'prev = '+str(prev)
        i=i+1

    return output

    

def pianorolls_to_midi2(piano_rolls, programs, fs=16 ):
    '''Converts Piano Rolls array to a PrettyMidi object
     with multiple instruments.
    
    Input:
    piano_roll :array of np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    programs : int array
        The program numbers of the instruments.
    
    Returns:
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.
    '''
    
      
    period=1./fs
    
    notes, frames = piano_rolls[0].shape #get number of frames in our piano roll
    pm = pretty_midi.PrettyMIDI() #create a Pretty Midi object
    
    for idx, currentinstrument in enumerate(programs):
        
        
        instrument=pretty_midi.Instrument(program=currentinstrument)
    
        #get processed pianoroll
        pianoarray=GetNoteArray(piano_rolls[idx])
        numsamenotes, frames= np.shape(pianoarray)
        
        for row in range(numsamenotes):
            
            notearray=pianoarray[row,:]
        
        
            prev_pitch=0
            prev_velocity=0
            notelength=0
            starttime=0
            endtime=period

            i=0
            while i<frames: #range over the frames of the piano roll

                #need to specify velocity (100 for note, 0 for rest),  start time, end time, and pitch
               
                #for ith column of piano roll get the (possible) non-zero index which
                #corresponds to the pitch
                
                            
                note=int(notearray[i])

                if note==0: #current is rest note, don't need to worry about length

                    velocity=0
                    starttime=i*period
                    endtime=period+i*period
                    current_pitch=0
                    pm_note=pretty_midi.Note(velocity=100, pitch=current_pitch, start=starttime, end=endtime)
                    i=i+1
                    instrument.notes.append(pm_note)

                else:

                    

                    #endtime=GetEndTime(i, note)


                    #get current pitch and set the start time
                    velocity=100
                    currnote=note

                    starttime=i*period


                    #loop over future notes to find when pitch changes
                    pitchchange=False
                    while pitchchange==False:

                        #if end of song quit
                        if i==frames-1:
                            endtime=period+i*period
                            break

                        #get next note
                        notenext=int(notearray[i+1])
                        
                        #if next note is a rest
                        if notenext==0: 
                            endtime=period+i*period
                            break

                        #if next frame has different pitch
                        elif notenext!=currnote: 
                            endtime=period+i*period
                            break

                        else:
                            #increment to next frame
                            i=i+1
                            #print i

                    pm_note=pretty_midi.Note(velocity=100, pitch=currnote, start=starttime, end=endtime)
                    i=i+1
                    #we have appended note, now move to next note   
                    instrument.notes.append(pm_note)
                #print starttime
                #print endtime

            pm.instruments.append(instrument)
        
    return pm



