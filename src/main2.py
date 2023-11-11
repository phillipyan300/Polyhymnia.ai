
import musicJudge.basicPitch as basicPitch
import musicJudge.NeedlemanWunschDiff as diff


"""
Part 2 of Main Pipeline: Once main1 finishes, waits for student to submit audio
Upon audio submission, then this part 2 will run

"""

def main(audioFile: str):
     #Get the stored correct notes from the markov.py
    file_path = 'musicGen/lilypond.txt'

    with open(file_path, 'r') as file:
        correctNotes = file.readline().strip()
    print(correctNotes)


    #Get the student's notes from the audio
    studentNotes = basicPitch.run(f"audioFiles/{audioFile}")
    print(studentNotes)

    #Perform the diff operation
    score = diff.run(correctNotes, studentNotes)
    #Return the score
    return score

if __name__ == "__main__":
    print(main("120HalfC.mp3"))


#Runs the markov.py to get the correct notes. 

#Gets the recording at some point
#Runs basicPitch to get the notes by the student
#Performs diff operation to get the score