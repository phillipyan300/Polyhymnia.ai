
import tensorflow as tf
from basic_pitch.inference import predict, predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


"""
How to Use: This is called in scoreFinder, which just needs to call pitchDected to get the lilypond form of the student recording
Input: filename
Output: lilypond string format of the student recording

Notes/Log: 
1. Don't use MIDI, not transcribed well
2. Seems like a cutoff on notes, test in demo playground
3. test save notes and build a diff operator with Needleman-Wunsch
4. Discretize the sounds over units of time, then do Needleman wunsch between optimal and student submission 

"""
#Takes in a mp3 file and returns the lilypond string format
#NOTE That this is the filepath, not the filename
def pitchDetect(filename: str) -> str:
    pitchToNote = {60: "c", 61: "cis", 62: "d", 63: "dis", 64: "e", 65: "f", 66: "fis", 67: "g", 68: "gis", 69: "a", 70: "ais", 71: "b", 72: "c'", 73: "cis'", 74: "d'", 75: "dis'", 76: "e'", 77: "f'", 78: "fis'", 79: "g'", 80: "gis'", 81: "a'", 82: "ais'", 83: "b'", 84: "c''"}
    # Define your minimum and maximum frequency values
    min_frequency = 258 # Your minimum frequency value in Hz, C4
    max_frequency = 1080 # Your maximum frequency value in Hz C6

    # Call the predict function with your audio path and frequency parameters
    model_output, midi_data, note_events = predict(
        filename,
        minimum_frequency = min_frequency,
        maximum_frequency = max_frequency,
        )

    # print(midi_data)
    # print(note_events)

    #Sort
    sorted_notes = sorted(note_events, key=lambda x: x[0])
    # for note in sorted_notes:
    #     print(str(note) + "\n")

    #Remove the last few columns
    final_notes = []
    for note in sorted_notes:
        # print(note)
        newNote = (note[0], note[1], pitchToNote[note[2]])
        final_notes.append(newNote)
    

    #Lets pretty print note events
    # for note in final_notes:
    #     print(note)

    returnString = _cleanPitch(final_notes)
    return returnString

#Converts the given pitches into lilypond so we can compare with the correctnotes
#Assumes 120 bpm
#Helper function to main pitch detect function
def _cleanPitch(notes: list):
    returnStr = ""
    prevEnd = 0
    for note in notes:
        #Give a 0.1 second buffer time, otherwise there is a rest
        start = note[0]
        if start > prevEnd + 0.1:
            restTime = _getNote(start-prevEnd)
            returnStr += f"r {restTime} "
        end = note[1]
        pitch = note[2]
        duration = end-start
        noteType = _getNote(duration)

        #combine the pitch with the duration
        returnStr += f"{pitch} {noteType} "
        prevEnd = end
    return returnStr


#Helper function, get the note type, assuming 120 bpm
def _getNote(duration: float) -> str:
    #print(duration)
    if 0 < duration <= 0.1875:
        noteType = "16"
    elif  0.1875 < duration <= 0.375:
        noteType = "8"
    elif 0.375 < duration <= 0.625:
        noteType = "4"
    elif 0.625 < duration <= 0.875:
        noteType = "4."
    elif 0.875 < duration <= 1.125:
        noteType = "2"
    else:
        noteType = "1"
        #Potential else for whole note
    return noteType

def run(filepath: str) -> str:
    return pitchDetect(filepath)

if __name__ == "__main__":
    print(pitchDetect("../audioFiles/120HalfC.mp3"))

# #In case we want to save data into a csv file
# predict_and_save(
#     ["/Users/phillipyan/Documents/hackprinceton2023/src/musicJudge/120QuarterC.mp3", "/Users/phillipyan/Documents/hackprinceton2023/src/musicJudge/120HalfC.mp3"],
#     ".",
#     minimum_frequency=min_frequency,
#     maximum_frequency=max_frequency,
#     save_midi = False,
#     sonify_midi = False,
#     save_model_outputs=False,
#     save_notes=True,
# )