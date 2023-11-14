# Polyhymnia.ai 

As an AI-powered application, Polyhymnia.ai gauges student musicians' proficiency with any instrument and offers infinitely generatable personalized sheet music based on their current skill level.

Built @ HackPrinceton 2023 by

Phillip Yan: Built the backend server, the Markov Chain-based generative algorithm for producing unique and melodic sheet music, and the AI and Needleman-Wunsh judging algorithm for grading student audio submissions.

Matthew Cheng: Planned and designed the front end interface with Figma and created the logo. 

Yash Shah: Setup the back end for user authentification and front end pages alongside the API routes. 


## Project introduction

Polyhymnia.ai is an application that allows users to gauge their skills with their choice of musical instrument and be given personalized sheet music based on their skill level so that they can improve at a gradual pace and be given individualized attention. It consists of two parts, first a generative section which constructs sheet music based on a Markov chain of note probabilities and another section which judges how well a student played the music in terms of pitch, rhythm and time.

Our project is a tool designed to help musicians of all skill levels assess their performances and improve their musical abilities, even without the help of a formal music tutor. We hope this helps make music education more accessible to all! 

## Project information
The application allows users to upload audio files and receive a comprehensive grade based on pitch, rhythm, and intonation, 
giving them a composite overview of their musical performance.

After each iteration, a user receives a grade for their inputted audio file, with generative model automatically adjusting the model to generate a harder or easier piece of sheet music based on performance. 

Our project includes innovative music generation methods based on several Markov Chains with parameterized values based on difficulty to procedurally generate melodies that closely replicate real composed music, but which also have an element of uniqueness and randomness.

Our project also utilizes the Needleman-Wunsch algorithm, taking inspiration from bioinformatics to innovatively provide an alignment method to standardize the judgement of submitted audio files.
