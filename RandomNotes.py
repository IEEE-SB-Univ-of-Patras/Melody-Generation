from sys import audit
import pretty_midi
import glob
import random
import numpy as np
import py_midicsv as pm

def GetMidiFiles(foldername):
    midiList = glob.glob(foldername)

    #random.shuffle(midiList)

    return midiList

def GenerateRandomNotes(n):

    listNotes = []

    for i in range(n):

        time = i * 100
        notePitch = random.randint(0, 100);
        noteVelocity = random.randint(50, 100);

        noteString_on = "2, {}, {}, 0, {}, {}\n".format(time, "Note_on_c", notePitch, noteVelocity);
        noteString_off = "2, {}, {}, 0, {}, {}\n".format(time + 100, "Note_off_c", notePitch, noteVelocity);

        listNotes.append(noteString_on)
        listNotes.append(noteString_off)

    return listNotes 


def main():

    #listMidis = GetMidiFiles("./MIDI_DATA/*.mid")

    #midiFile = listMidis[0]
    #midiFile = "./MIDI_DATA/#Test.mid"

    noteStrings = GenerateRandomNotes(20);

    print(noteStrings)
    
    with open("randomnotes.csv", "w") as f:
      f.write("0, 0, Header, 1, 2, 384\n")
      f.write("2, 0, Start_track\n")

      f.write("2, 0, Program_c, 0, 0\n")
      
      f.writelines(noteStrings)

      f.write("2, 5000, End_track\n")
      f.write("0, 0, End_of_file\n")

    #MidiToString(midiFile)

    # Parse the CSV output of the previous command back into a MIDI file
    midi_object = pm.csv_to_midi("randomnotes.csv")

    # Save the parsed MIDI file to disk
    with open("example.mid", "wb") as output_file:
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)


    midiFormat = pretty_midi.PrettyMIDI("example.mid")
    audio_data = midiFormat.synthesize(wave = np.sin)
     
    from scipy.io.wavfile import write
 
    write("test.wav", 44100, audio_data)



if __name__ == "__main__":
    main()
