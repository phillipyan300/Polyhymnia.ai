from flask import Flask, request
import os

app = Flask(__name__)

# You can set a specific folder to save uploaded files
UPLOAD_FOLDER = '/Users/yashshah/Desktop/HackPrinceton2023/hackprinceton2023/my-app/musicFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'audio' not in request.files:
        return 'No file part', 400

    file = request.files['audio']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file', 400

    if file:    
        filename = secure _filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return 'File uploaded successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
