from flask import Flask, request, jsonify, send_file
from src.main1 import main as main1
from src.main2 import main as main2
from pdf2image import convert_from_path



app = Flask(__name__)

# Endpoint for receiving a number and updating the sheet image and sending
# Number needs to between 0 and 1
@app.route('/generate-image', methods=['POST'])
def generateImage():
    data = request.get_json()
    print(data)
    #Default is 0.2 assuming there is no number sent
    number = data.get('number', 0.2)

    #Generate the sheet music (I think this should work)
    main1(number)

    #Obtain the sheet music working directory
    file_path = 'src/musicGen/my_music.pdf'

    # convert pdf to png (not sure if I need to save)
    image = convert_from_path(file_path)

    # send the png 
    return send_file(image, mimetype='image/png')

#Endpoint for receiving an audio file and returning a number
@app.route('/process-audio', methods=['POST'])
def returnScore():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio part"}), 400
    audio = request.files['audio']

    #Process the audio and perform transcription...
    #For example, `result = transcribe_audio(audio)`
    #...

    #Example response with a number (e.g., analysis result)
    return jsonify({"result": 123}), 200



if __name__ == '__main__':
    app.run(debug=True)


# Endpoint for receiving an audio file and returning a number
@app.route('/process-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file found"}), 400

    audio_file = request.files['audio']

    # Process the audio file
    result = main2(audio_file)

    return jsonify({"result": 123}), 200

if __name__ == '__main__':
    app.run(debug=True)
