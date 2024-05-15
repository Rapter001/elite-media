import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('view_files'))
    return render_template('upload.html')

@app.route('/view')
def view_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view.html', files=files, upload_folder='uploads')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open(os.path.join(os.path.dirname(__file__), 'contact-us-data.txt'), 'a') as f:
            f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n\n")
        return redirect(url_for('thank_you'))
    return render_template('contact-us.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/contact-us-data')
def view_contact_data():
    with open(os.path.join(os.path.dirname(__file__), 'contact-us-data.txt'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    formatted_data = []
    for i in range(0, len(lines), 3):
        formatted_data.append('<br>'.join(lines[i:i+3]))
    formatted_data = '<br><br>'.join(formatted_data)
    return formatted_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="84", debug=False)
