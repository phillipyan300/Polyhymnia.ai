

"""
Description: Runs the Needleman Wunsch on two lilypond notation files and returns a percentage score as the diff. 

Specifically, algo runs diff operation twice, once on pitch and the other on rhythm
CAPABILITY TO CHANGE EMPHASIS (like if a student wants to practice more rhythem or pitch)


Input: Two lilypond notation files
Output: The diff score (0-1) with 0 being totally wrong, 1 being completely the same
"""

#Dynamic Programming alg for Needleman Wunsch
def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_score=-1) -> tuple:
    # Create a scoring matrix
    m, n = len(seq1), len(seq2)
    score = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Initialize scoring matrix and traceback path
    for i in range(m + 1):
        score[i][0] = gap_score * i
    for j in range(n + 1):
        score[0][j] = gap_score * j

    # Fill in the scoring matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score)
            delete = score[i-1][j] + gap_score
            insert = score[i][j-1] + gap_score
            score[i][j] = max(match, delete, insert)

    # Traceback and compute the alignment 
    align1, align2 = '', ''
    i, j = m, n
    while i > 0 or j > 0:
        current_score = score[i][j]
        if i > 0 and j > 0 and current_score == score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score):
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif i > 0 and current_score == score[i-1][j] + gap_score:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
        else:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1

    # Reverse the alignments as we've built them backwards
    align1 = align1[::-1]
    align2 = align2[::-1]

    final_score = score[m][n]  # The final score is in the bottom-right corner of the matrix
    return align1, align2, final_score

#Clean input data the and return the pitches and rhythms list


def runNeedlemans(correctStr: str, studentStr: str) -> int:
    #print(correctStr)
    #print(studentStr)
    min = needleman_wunsch(correctStr, "")[2]
    max = needleman_wunsch(correctStr, correctStr)[2]
    #Basically making everything positive for easier division. Min is 0, max is max+min
    raw = needleman_wunsch(correctStr, studentStr)[2] + abs(min)
    score = raw / (abs(min) + abs(max))
    if score < 0:
        score = 0
    #print(score)

    return score



def cleanPitch(noteStr: str) -> str:
    returnStr = ""
    #Convert multicharracter elements of the note string into single elements
    hashMap = {"c": 'a', "cis": 'b', "d" : 'c', "dis": 'd', "e": 'e',
                              "f": 'f', "fis": 'g', "g": 'h',  "gis": 'i',  "a": 'j',  
                              "ais": 'k', "b" :'l',  "c'": 'a',  "cis'":'b',  "d'":'c',  
                              "dis'":'d',  "e'": 'e',  "f'": 'f',  "fis'":'g',  "g'":'h',  
                              "gis'":'i',  "a'": 'j',  "ais'" :'k', "b'": 'l',  "c''": 'a'
                              }  #Don't forget about the rest!!

    split = noteStr.split(" ")
    for i in range(0, len(split), 2):
        if split[i] in hashMap:
            encodedChar = hashMap[split[i]]
            returnStr += encodedChar
        #If it is a space
        else:
            continue
    return returnStr

def cleanRhythm(noteStr: str) -> str:
    returnStr = ""
    #convert multicharacter elements of the rhythm into single elements
    hashMap = {"16": 'a',  "8": 'b', "4":'c', "4.": 'd', "2": 'e', "1": 'f'}
    split = noteStr.split(" ")

    #remove rests
    updatedSplit = []
    for i in range(0, len(split), 2):
        if i+1 < len(split):
            if split[i] == "r":
                continue
            else:
                updatedSplit.append(split[i])
                updatedSplit.append(split[i+1])

                
    for i in range(1, len(updatedSplit), 2):
        if updatedSplit[i] in hashMap:
            encodedChar = hashMap[updatedSplit[i]]
            returnStr += encodedChar
    return returnStr


#Returns needleman Wunsch score
def run(correctStr: str, studentStr: str) -> int:
    blendFactor = 1.01


    rhythmCorrect = cleanRhythm(correctStr)
    rhythmStudent = cleanRhythm(studentStr)
    print("Rhythm Correct")
    print(rhythmCorrect)
    print("Rhythm Student")
    print(rhythmStudent)
    


    pitchCorrect = cleanPitch(correctStr)
    pitchStudent = cleanPitch(studentStr)
    
    print("Pitch Correct")
    print(pitchCorrect)
    print("Pitch Student")
    print(pitchStudent)

    rhythmScore = runNeedlemans(rhythmCorrect, rhythmStudent)
    rhythmScore = rhythmScore * (1-blendFactor)
    pitchScore = runNeedlemans(pitchCorrect, pitchStudent)




    #Alternatively, can return both scores

    return (rhythmScore + pitchScore) / (blendFactor)



if __name__ == "__main__":
    # Test Case 1: Perfect match
    correct_str1 = "f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4"
    student_str1 = "f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4"
    # print(run(correct_str1, student_str1))  # Expected: Close to 1

    # Test Case 2: Completely different
    correct_str2 = "f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4"
    student_str2 = "a 16 b 16 c 16 d 16 e 16 f 16 g 16 a 16 b 16 c 16 d 16 e 16 f 16 g 16 a 16"
    # print(run(correct_str2, student_str2))  # Expected: Close to 0

    # Test Case 3: Partial match
    correct_str3 = "f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4"
    student_str3 = "f 8 fis 8 b 8 g 4 f 8 dis 4 a 8 a 8 b 8 c 8 r4. d 8 e 4. f 2 g 8 h 4. i 8 j 4"
    # print(run(correct_str3, student_str3))  # Expected: A score between 0 and 1

    # Test Case 4: One empty string
    correct_str4 = "f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4"
    student_str4 = ""
    # print(run(correct_str4, student_str4))  # Expected: Close to 0

# Additional test cases can be added to cover more scenarios, 
# including variations in rhythm and pitch.

#Test case:
#print(run("f 8 fis 8 b 8 g 4 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4 ", "f 8 fis 8 fis 8 f 8 dis 4 c' 8 c' 8 g 8 fis 8 r4. g 8 g 4. ais 2 ais 8 dis 4. f 8 dis 4 "))

# # Example usage
# seq1 = "GATTACA"
# seq2 = "GCATGCU"
# align1, align2, final_score = needleman_wunsch(seq1, seq2)
# print("Alignment 1:", align1)
# print("Alignment 2:", align2)
# print("Final Score:", final_score)

# #Worst case scenerio
# seq1 = ""
# seq2 = "GCATGCU"
# align1, align2, final_score = needleman_wunsch(seq1, seq2)
# print("Alignment 1:", align1)
# print("Alignment 2:", align2)
# print("Final Score:", final_score)

# #Best case scenerio
# seq1 = "GCATGCU"
# seq2 = "GCATGCU"
# align1, align2, final_score = needleman_wunsch(seq1, seq2)
# print("Alignment 1:", align1)
# print("Alignment 2:", align2)
# print("Final Score:", final_score)


