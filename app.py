from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from plate_recognition import plate_recognizer


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        # Save the uploaded image
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        new_image_path=plate_recognizer(app,image_path)
        return render_template('submit.html',image_path=image_path,
                               modified_image_path=new_image_path)
    return render_template('submit.html')

if __name__ == '__main__':
    app.run()