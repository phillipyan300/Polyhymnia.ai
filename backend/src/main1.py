import musicGen.markov as markov
"""
Runs Markov to get a new sheet music
Input: Difficulty level
Output: A new sheet music

Currently just generating 4 measures

"""
def main(difficulty: float):
    #Generate 4 measures
    markov.run(20, difficulty)
    #Can grab the lilypond pdf from the gen folder

if __name__ == "__main__":
    print(main(0.5))
