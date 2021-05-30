import py_midicsv
import pretty_midi
import numpy as np

from scipy.io.wavfile import write

def MidiFileToString(filename): # Turn the MIDI into the format that will be inserted into the neural network.

    csv_string = py_midicsv.midi_to_csv(filename)

    noteOnString = "Note_on_c"
    noteOffString = "Note_off_c"
    eofString = "End_of_file"


    def IsEvent(noteInfo):
        return noteInfo[2].strip() == noteOnString or noteInfo[2].strip() == noteOffString

    finalString = ""

    current_time = 0

    scanningTimeframe = False

    print(csv_string)

    for line in csv_string:

        noteInfo = line.split(",")

        if (current_time == noteInfo[1]):

            if not scanningTimeframe:
                #finalString += "$ "
                scanningTimeframe = True
        else:

            timeDt = int(noteInfo[1]) - int(current_time)

            if (timeDt > 0):
                finalString += "{}t ".format( int(noteInfo[1]) - int(current_time) )
                scanningTimeframe = True

                current_time = noteInfo[1]

        if (IsEvent(noteInfo)):

            if (noteInfo[2].strip() == noteOnString):
                finalString += "{} ".format(int(noteInfo[4]))
            elif (noteInfo[2].strip() == noteOffString):
                finalString += "{}e ".format(int(noteInfo[4]))
        
        elif noteInfo[2].strip() == eofString:
            return finalString

        
    return finalString

def StringToNotes(s): # Turn the list of Notes into a string that will be written into a CSV file.
    
    noteTokens = s.split(" ")

    listNoteStrings = []

    time = 0
    
    listNoteStrings.append( "0, 0, Header, 1, 2, 384\n" )
    listNoteStrings.append( "2, 0, Start_track\n" )
    listNoteStrings.append( "2, 0, Program_c, 0, 0\n" )
    
    for note in noteTokens :

        if (len(note) == 0): continue

        if note[-1] == 't':

            time += int( note[:-1] )

        elif note[-1] == 'e':
            
            noteString = "2, {}, {}, 0, {}, {}\n".format(time, "Note_off_c", note[:-1], 100)
            listNoteStrings.append(noteString)

        elif note.isnumeric():

            noteString = "2, {}, {}, 0, {}, {}\n".format(time, "Note_on_c", note, 100)
            listNoteStrings.append(noteString)

    listNoteStrings.append( "2, {}, End_track\n".format(time) )
    listNoteStrings.append("0, 0, End_of_file\n")

    return listNoteStrings

def NotesToCsv(l, filename):

    with open(filename, "w") as csvFile:
        csvFile.writelines(l)

def CsvToMidi(filename): # Turn the CSV file back into MIDI

    midiObject = py_midicsv.csv_to_midi(filename)

    # Save the MIDI file

    with open("{}.mid".format(filename), "wb") as midiFile:

        midiWriter = py_midicsv.FileWriter(midiFile)
        midiWriter.write(midiObject)
    
def MidiToWav(filename): # Finally synthesize the MIDI into a WAV sound file.

    midiFormat = pretty_midi.PrettyMIDI(filename)
    audioData = midiFormat.synthesize(wave = np.sin)
    write(filename + ".wav", 44100, audioData)

def StringToWav(s, name):

    l = StringToNotes(s)
    NotesToCsv(l, name + ".csv")
    CsvToMidi(name + ".csv")
    MidiToWav(name + ".csv.mid")

def main():
    
    s = MidiFileToString("./MIDI_DATA/109 Boss.mid")

    print(s)

    StringToWav(s, "vagos")

        
main()
