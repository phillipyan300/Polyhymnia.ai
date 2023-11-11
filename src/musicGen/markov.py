import random 
from midiutil import MIDIFile
import os
import pygame
import time


"""
Purpose: 
1. Uses a markov chain to generate a random walk for a given set of potential notes.
2. Converts notes to a midi file "output.mid"
3. Converts note to a lilypond file "my_music.ly"
4. Converts lilypond file to pdf stored in the same directory as "my_music.pdf"


#Issues: 
1.  Lily wrong length sometimes (not example 4/4) will need to consider fitting into 4/4 and considering slurring across measures

"""

# Generate a random note: Returns the string note and the float length
def generateNote(seedNote: str, seedLength: str) -> str:
    #print(seedNote)
    #print(seedLength)
    # Generate Notes
    noteArray = ["C'", "Eb", "F", "F#", "G", "Bb", "C''", "Rest"]
    lengthArray = [0.25, 0.5, 1, 1.5, 2]

    #Keep rests probability constant at 0.1
    #Penalty for jumps
    #G works well with everything
    
    note_markov_chain = [
        [0.2, 0.25, 0.2, 0.05, 0.1, 0.05, 0.05, 0.1], # C4
        [0.225, 0.2, 0.225, 0.05, 0.1, 0.05, 0.05, 0.1], # E-flat
        [0.05, 0.225, 0.2, 0.225, 0.1, 0.05, 0.05, 0.1], # F
        [0.05, 0.05, 0.25, 0.2, 0.25, 0.05, 0.05, 0.1], # F#
        [0.05, 0.05, 0.05, 0.25, 0.2, 0.25, 0.05, 0.1], # G
        [0.05, 0.05, 0.05, 0.05, 0.25, 0.2, 0.25, 0.1], # B-flat
        [0.05, 0.05, 0.05, 0.05, 0.2, 0.3, 0.2, 0.1], # C5
        [0.2, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1], # Rest
    ]

    length_markov_chain = [
        [0.00, 0.5, 0.2, 0.2, 0.1], # 0.25
        [0.00, 0.5, 0.2, 0.2, 0.1], # 0.5
        [0.00, 0.5, 0.2, 0.2, 0.1], # 1
        [0.00, 0.5, 0.2, 0.2, 0.1], # 1.5
        [0.00, 0.5, 0.2, 0.2, 0.1], # 2
    ]

    
    #Generate a random note
    startNote = noteArray.index(seedNote)
    #Generates a random number between 0 and 1 to use to simulate random walk
    randomNumber = random.random()
    runningTotalHelper = 0
    #Iterate through that row of the markov chain and find the next note
    for index, currNote in enumerate(note_markov_chain[startNote]):
        runningTotalHelper += currNote
        if randomNumber <= runningTotalHelper:
            #print("nextNote")
            nextNote = noteArray[index]
            break
    
    #Generate a random length
    startLength = lengthArray.index(seedLength)
    #Generates a random number between 0 and 1 to use to simulate random walk
    randomNumber = random.random()

    #print(f"random {randomNumber}")
    runningTotalHelper = 0
    #Iterate through that row of the markov chain and find the next note
    for index, currLength in enumerate(length_markov_chain[startLength]):
        runningTotalHelper += currLength
        #print(f"runningTotal {runningTotalHelper}")
        if randomNumber <= runningTotalHelper:
            #print("nextLength")
            nextLength = lengthArray[index]
            break 

    return (nextNote, nextLength)


# Measures need to be at least 1
def generateMelody(measures: int) -> list[tuple[str, int, int]]:
    potentialNotes = {"C'": 60, "Eb": 63, "F": 65, "F#": 66, "G": 67, "Bb": 70, "C''": 72, "Rest": "Rest"}
    melody = []
    totalLength = measures * 4
    currBeat = 0
    note = "C'"
    length = 1
    #While there are at least two beats left
    while currBeat < totalLength-2:
        info = generateNote(note, length)
        note = info[0]
        length = info[1]

        #If the note is a rest, then we can just add it
        if note == "Rest":
            currBeat += length
            continue

        #Otherwise, we append the note and its start and end
        melody.append((potentialNotes[note], currBeat, currBeat+length))
        currBeat += length
    return melody

#generates both a midi file and a lilypond file
def generate(measures: int) -> str:
    # List of notes. Each note is a tuple with (pitch, time, duration).
    # For example: (60, 0, 1) is middle C, at the beginning, lasting 1 beat.
    notes = generateMelody(measures)
    #print(notes)
    generateMid(notes, measures)
    generateLily(notes)
    lilyToPDF("my_music.ly")
    return "MIDI and LilyPond files have been generated."
    


def generateMid(notes: list, measures: int):
    # Create a MIDIFile object with one track
    midi_file = MIDIFile(1)

    # Add some setup information
    track = 0   # The only track in this case
    time = 0    # Start at the beginning
    midi_file.addTrackName(track, time, "Sample Track")
    midi_file.addTempo(track, time, 120)  # Set the tempo to 120 Beats Per Minute

    channel = 0
    volume = 100  # 0-127, as per the MIDI standard

    # Add notes to the MIDI file
    for note in notes:
        pitch, time, duration = note
        midi_file.addNote(track, channel, pitch, time, duration, volume)


    # Write the MIDI file to disk
    with open("output.mid", "wb") as output_file:
        midi_file.writeFile(output_file)
    return "MIDI file has been written to 'output.mid'"

#This generates the lilypond file which, when run, produces sheet music
def generateLily(notes: list):
    toLilyNote = {60: "c", 61: "cis", 62: "d", 63: "dis", 64: "e", 65: "f", 66: "fis", 67: "g", 68: "gis", 69: "a", 70: "ais", 71: "b", 72: "c'", 73: "cis'", 74: "d'", 75: "dis'", 76: "e'", 77: "f'", 78: "fis'", 79: "g'", 80: "gis'", 81: "a'", 82: "ais'", 83: "b'"}
    toLilyLength = {0.25: "16", 0.5: "8", 1: "4", 1.5: "4.", 2: "2"}
    print(notes)
    prevEnd = 0
    lilyNote = ""
    for note in notes:
        pitch, start, end = note
        duration = end-start

        #Need to first check if there was a gap between the start here and end (this represents a rest)
        if start != prevEnd:
            lilyNote += "r"
            lilyNote += toLilyLength[start-prevEnd]
            lilyNote += " "
        #Convert the note to lily note
        lilyNote += toLilyNote[pitch]
        lilyNote += " "

        #Convert the duration to lily duration
        lilyNote += toLilyLength[duration]
        lilyNote += " "

        prevEnd = end
    
    #print(lilyNote)

    lilypond_notation = f"""
    \\version "2.20.0"

    \score {{
    \\fixed c' {{
        \clef treble
        \key c \major
        \\time 4/4

        {lilyNote}
    }}
    }}
"""
    
    #print(lilypond_notation)

    filename = "my_music.ly"

    with open(filename, 'w') as file:
        file.write(lilypond_notation)

    print(f"LilyPond file '{filename}' has been created.")


#This function takes a lilypond file and converts it to a pdf
def lilyToPDF(filename: str):
    #print(filename)
    print(filename[:-3])
    print(filename[:-3] + ".pdf")
    os.system(f"lilypond {filename}")
    #os.system(f"open {filename[:-3]}.pdf")

def play(filename: str):
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)

    # Play the MIDI file
    pygame.mixer.music.play()

    # You can use pygame.event.wait() to wait for the music to finish playing,
    # but here we'll use a simple time.sleep() loop to wait until the music is done
    while pygame.mixer.music.get_busy():
        time.sleep(1)


def run(measures: int):
    print(generate(measures))
    os.system(f"open my_music.pdf")
    play("output.mid")
    print("Done playing")




 


if __name__ == "__main__":
    print(run(4))



    

#Markov rules
    # Distance penalty
    # Benefit for arpeggios and blues note (f sharp)

    # Syncopation benefits
    # Repeated notes benefit
    # Repeated patterns benefit


    # arpeggios and key base notes benefit
    # jazz swing (triplet feel) means for eight should be 0.66 and 0.34

    # Maybe hide a few licks in there. Blues licks generator