import numpy as np
import pretty_midi 

def pianoroll_to_midi(piano_roll, fs=16, program=0):
    '''Converts a Piano Roll array to a PrettyMidi object
     with a single instrument.
    
    Input:
    piano_roll : np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    program : int
        The program number of the instrument.
    
    Returns:
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.
    '''
    period=1./fs
    
    notes, frames = piano_roll.shape #get number of frames in our piano roll
    pm = pretty_midi.PrettyMIDI() #create a Pretty Midi object
    instrument = pretty_midi.Instrument(program=0) #specify our instrument

    #record previous pitch/velocity so we can concatenate notes together
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
        col=piano_roll[:,i] 
        colnext=piano_roll[:,i+1]
        tmp=np.nonzero(col)
        tmpnext=np.nonzero(colnext)
        
        if tmp[0].size==0: #current is rest note, don't need to worry about length
            
            velocity=0
            starttime=i*period
            endtime=period+i*period
            current_pitch=0
           
        
        else:
            #get current pitch and set the start time
            velocity=100
            current_pitch=tmp[0][0]
            starttime=i*period
            
            
            #loop over future notes to find when pitch changes
            pitchchange=False
            while pitchchange==False:
                
                #if end of song quit
                if i==frames-1:
                    endtime=period+i*period
                    break
                    
                #get next note
                colnext=piano_roll[:,i+1]
                tmpnext=np.nonzero(colnext)
                
                #if next note is a rest
                if tmpnext[0].size==0: 
                    endtime=period+i*period
                    break
                    
                #if next frame has different pitch
                elif tmpnext[0][0]!=current_pitch: 
                    endtime=period+i*period
                    pitchchange=True
            
                else:
                    #increment to next frame
                    i=i+1
                    
            
        pm_note=pretty_midi.Note(velocity=100, pitch=current_pitch, start=starttime, end=endtime)
        i=i+1
        #we have appended note, now move to next note   
        instrument.notes.append(pm_note)
        #print starttime
        #print endtime
        
    pm.instruments.append(instrument)

    return pm