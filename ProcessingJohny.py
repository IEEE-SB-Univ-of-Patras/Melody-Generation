#from sys import audit
#import glob
#import random
import numpy as np
import py_midicsv
import pretty_midi
#from tensorflow import keras
#from tensorflow.keras import layers
from scipy.io.wavfile import write
#import numpy as np
#import random
#import io
import time


OutputName = ""

def myFunc(x):
    return int(x.split(",")[1])
def StringToCSV(String):
    accuracy=180
    lmao=accuracy
    channel=1
    velocity=50
    state=1
    while(state==1):
        String2=String.replace("aa","a")
        String2=String2.replace("  "," ")
        
        if len(String2)==len(String):
            state=0
        else:
            state=1
        String=String2
    

        
    midi_length=String.count(" ")
    time_list=[]
    #initialize time list
    for i in range(0,midi_length+2):
      time_list.append([])
    temp_list=String.split(" ")
    k=-1
    for i in temp_list:
        
        temp_list2=i.split("a")
        temp_list2.pop(0)
        time_list[k]=temp_list2
        k=k+1

    #time list filled
    for i in range(0,len(time_list)):
        time_list[i]=list(dict.fromkeys(time_list[i]))
    print("FILTERED:",time_list)
    results_table=[]
    results_table.append( "0, 0, Header, 1, 2, 384\n" )
    results_table.append( "2, 0, Start_track\n" )
    results_table.append( "2, 0, Program_c, 0, 0\n" )

    
        ######
    for i in range(0,len(time_list)):
        for j in time_list[i]:
            ######
            note=""

            for k in range(i,len(time_list)-1):
                if j in time_list[k]:
                    time_list[k].remove(j)
                else:
                    end=k
                    
                    start=i
                    note=j
                    break
            if note!="":
                if int(note)<=90 :
                    note_safe=int(note)
                else:
                    note_safe=0
                if int(note)<=3:
                    note_safe=0
            else:
                note_safe=0
            if note_safe==0:
                pass
            else:
                results_table.append("{}, {}, Note_on_c, 0, {}, {}\n".format(channel,int(start)*lmao,note_safe,velocity))
                results_table.append("{}, {}, Note_off_c, 0, {}, {}\n".format(channel,int(end)*lmao,note_safe,velocity))
                    
    results_table.sort(key=myFunc, reverse=False)

    
    
    #!!!!!!! tail of midi , metadata 
    results_table.append( "2, {}, End_track\n".format(int(end)*lmao) )
    results_table.append("0, 0, End_of_file\n")
    #!!!!!!! propably incorrect for other files
    
    
        
    return results_table
            


def NotesToCsv(l, filename):

    with open(filename, "w") as csvFile:
        csvFile.writelines(l)

def CsvToMidi(filename):

    midiObject = py_midicsv.csv_to_midi(filename)

    # Save the MIDI file

    with open("{}.mid".format(filename), "wb") as midiFile:

        midiWriter = py_midicsv.FileWriter(midiFile)
        midiWriter.write(midiObject)

def MidiToWav(filename, outputname): # Finally synthesize the MIDI into a WAV sound file.

    midiFormat = pretty_midi.PrettyMIDI(filename)
    audioData = midiFormat.synthesize(wave = np.sin)
    write(outputname + ".wav", 44100, audioData)




    
def MidiFileToString(filename):
    accuracy=10
    

    csv_string = py_midicsv.midi_to_csv(filename)
    csv_string2=csv_string
    print(csv_string)
    csv_string=[]

    for line in csv_string2:
        if 1==1:
        
            if "Note_on_c" in line:
                csv_string.append(line)
            if "Note_off_c" in line:
                csv_string.append(line)


    midi_length=csv_string[-1].split(",")
    midi_length=int(midi_length[1])
    csv_string.pop(-1)
    
    time_list=[]
    #initialize time list
    for i in range(0,midi_length):
      time_list.append([])


    #iterate through midi file (string form)
    
    for line in csv_string:
        
        
        noteInfo= line.split(",")
        start=noteInfo[1].strip()

        #if you encounter a note starting then find when it ends
        end=midi_length
        if noteInfo[2].strip()=="Note_on_c":
            
            current_note=noteInfo[4].strip()
           
            for line2 in csv_string:
              
              noteInfo2= line2.split(",")
 
              if (int(noteInfo2[4].strip())==int(current_note.strip())) and (noteInfo2[2].strip()=="Note_off_c") and (int(noteInfo2[1])>int(start)):
                end=noteInfo2[1].strip()
                break
        #after you found starting and ending timeframes of note add the note to the timelist
           
            for i in range(int(start),int(end)):
                time_list[i].append(str(current_note))


    #take list and make string with a
    string=""
    for i in range(0,len(time_list),accuracy):
        string=string+" "
        for j in time_list[i]:
            string=string+"a"+j
    
    return string

def StringToWav(generated, filename):
    
    global OutputName

    result=StringToCSV(generated)
    NotesToCsv(result,"./Temp/{}.csv".format(filename))
    CsvToMidi("./Temp/{}.csv".format(filename))
    try:
        MidiToWav("./Temp/{}.csv.mid".format(filename), "./Final/" + OutputName)
    except:
        print("Couldn't make WAV")

def SetOutputName(name):

    global OutputName

    OutputName = name
    
def main():
    s1=time.time()
    noteString = MidiFileToString("ioanna.mid")
    print("hi")
    print(noteString)
    
    result=StringToCSV(noteString)
    print("hi")
    NotesToCsv(result,"my_product3.csv")
    print("hi")
    CsvToMidi("my_product3.csv")
    print("hi")
    MidiToWav("my_product3.csv.mid")
    s2=time.time()
    print(s2-s1)
    


if __name__ == "__main__":
    main()
