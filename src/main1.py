import musicGen.markov as markov
"""
Runs Markov to get a new sheet music
Input: Difficulty level
Output: A new sheet music

Currently just generating 4 measures

"""
def main(difficulty: float):
    #Generate 4 measures
    markov.run(4, difficulty)
    #Can grab the lilypond pdf from the gen folder

