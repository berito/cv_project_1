from flask import Flask, render_template, request,redirect,url_for,session
import os
import cv2
from werkzeug.utils import secure_filename
from plate_recognition import plate_identify


app = Flask(__name__)
app.secret_key = 'my secret'
@app.route('/')
def index():
    return 'Hello, World!'

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        # Save the uploaded image
        orginal_image_filename = secure_filename(image.filename)
        orginal_image_path = os.path.join(app.config['UPLOAD_FOLDER'], orginal_image_filename)
        image.save(orginal_image_path)
        
        # file names 
        new_image_filename = 'generated_image.jpg'
        edge_image_filename='edge_image.jpg'
        cropped_image_filename='cropped_image.jpg'
        merged_image_filename='merged_image.jpg'
        # file paths
        new_image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_filename)
        edge_image_path = os.path.join(app.config['UPLOAD_FOLDER'],edge_image_filename)
        cropped_image_path = os.path.join(app.config['UPLOAD_FOLDER'],cropped_image_filename)
        merged_image_path = os.path.join(app.config['UPLOAD_FOLDER'],merged_image_filename)
       
        decoded_image,edge_image,cropped_image,merged_image,text=plate_identify(orginal_image_path)
        # saving files
        cv2.imwrite(new_image_path, decoded_image) 
        cv2.imwrite(edge_image_path, edge_image) 
        cv2.imwrite(cropped_image_path, cropped_image) 
        cv2.imwrite(merged_image_path, merged_image) 
        
        session['new_image_filename'] = new_image_filename   
        session['orginal_image_filename']=orginal_image_filename
        session['edge_image_filename']=edge_image_filename
        session['cropped_image_filename']= cropped_image_filename
        session['merged_image_filename']= merged_image_filename
        return redirect(url_for('result'))
    return render_template('submit.html')
@app.route('/result')
def result():
    # Retrieve the result from the query parameter
    orginal_image_filename = session.get('orginal_image_filename')
    new_image_filename = session.get('new_image_filename')
    edge_image_filename = session.get('edge_image_filename')
    cropped_image_filename = session.get('cropped_image_filename')
    merged_image_filename = session.get('merged_image_filename')
    # print(orginal_image_filename)
    if  orginal_image_filename:
       orginal_image_path = os.path.join(app.config['UPLOAD_FOLDER'],  orginal_image_filename)
       new_image_path = os.path.join(app.config['UPLOAD_FOLDER'],  new_image_filename)
       edge_image_path = os.path.join(app.config['UPLOAD_FOLDER'],  edge_image_filename)
       cropped_image_path = os.path.join(app.config['UPLOAD_FOLDER'],  cropped_image_filename)
       merged_image_path = os.path.join(app.config['UPLOAD_FOLDER'],  merged_image_filename)
       return render_template('result.html',
                              orginal_image_path=orginal_image_path,
                              new_image_path=new_image_path,
                              edge_image_path=edge_image_path,
                              cropped_image_path=cropped_image_path,
                              merged_image_path=merged_image_path)
    else:
        return 'No image uploaded yet.'

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
    print('test')