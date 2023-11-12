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

<<<<<<< HEAD:src/main1.py
=======
if __name__ == "__main__":
    print(main(0.5))
>>>>>>> dfc0aaced97938f5218bce8ecd26910a2134e8bc:backend/src/main1.py
