import os
import smtplib
import requests
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.exceptions import RequestEntityTooLarge
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'svg', 'gif', 'mp4', 'webp', 'ogg', 'webm', 'bmp'}
# ADD YOUR SECRET KEY HERE
app.secret_key = ""
# ADD YOUR SECRET KEY HERE

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    :param filename: Name of the file to check.
    :return: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_error(error):
    """
    Handle the error when the uploaded file is too large.
    :param error: The error object.
    :return: Redirect to the upload page with an error message.
    """
    flash('File is too large. Maximum size allowed is 10 MB.', 'error')
    return redirect(url_for('upload'))

@app.route('/')
def index():
    """
    Render the index page.
    :return: The index.html template.
    """
    return render_template('index.html')

@app.route('/home')
def home():
    """
    Render the home page and list uploaded files.
    :return: The home.html template with the list of files.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handle file upload.
    If the request method is POST, save the uploaded file if it is allowed.
    :return: The upload.html template.
    """
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File uploaded successfully!', 'success')
                except Exception as e:
                    flash('Error uploading file. Please try again.', 'error')
            else:
                flash('File type not allowed. Please upload a file of allowed type.', 'error')
        else:
            flash('No file selected. Please choose a file to upload.', 'error')
    return render_template('upload.html')

@app.route('/view')
def view_files():
    """
    View the list of uploaded files.
    :return: The view.html template with the list of files.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view.html', files=files, upload_folder='uploads')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve an uploaded file.
    :param filename: Name of the file to serve.
    :return: The file from the upload directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view/<filename>')
def view_file(filename):
    """
    Serve a file for viewing.
    :param filename: Name of the file to view.
    :return: The file from the upload directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# hCaptcha secret key for verifying the captcha response
# ADD YOUR HCAPTCHA SECRET KEY HERE
hcaptcha_secret_key = ""
# ADD YOUR HCAPTCHA SECRET KEY HERE

@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    """
    Handle the contact us form submission.
    If the request method is POST, verify the hCaptcha response and send an email.
    :return: The contact-us.html template or redirect to the sent page.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        hcaptcha_response = request.form.get('h-captcha-response')

        # Check if the hCaptcha response is present
        if not hcaptcha_response:
            flash('hCaptcha verification is required. Please complete the captcha.')
            return render_template('contact-us.html')

        # Verify hCaptcha response
        data = {
            'secret': hcaptcha_secret_key,
            'response': hcaptcha_response
        }
        verify_response = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = verify_response.json()

        if result['success']:
            # ADD YOUR EMAIL DATA HERE
            sender_email = ""
            sender_password = ""
            receiver_email = ""
            # ADD YOUR EMAIL DATA HERE

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Elite Media Contact Us Form Submission"
        
            body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            msg.attach(MIMEText(body, 'plain'))
        
            try:
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()
            except Exception as e:
                flash(f'An error occurred while sending the form: {str(e)}')
                return render_template('contact-us.html')
        
            return redirect(url_for('sent'))
        else:
            flash('hCaptcha verification failed. Please try again.')

    return render_template('contact-us.html')

@app.route('/sent')
def sent():
    """
    Render the sent confirmation page.
    :return: The sent.html template.
    """
    return render_template('sent.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=False, threaded=True)
