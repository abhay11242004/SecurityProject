from flask import Flask, render_template, request, redirect, url_for
import os
from ciphers import encrypt_image, decrypt_image

app = Flask(__name__)
BASE_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ENCRYPTED_FOLDER = os.path.join(BASE_DIR, 'static', 'encrypted')
DECRYPTED_FOLDER = os.path.join(BASE_DIR, 'static', 'decrypted')

# Set Flask configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['DECRYPTED_FOLDER'] = DECRYPTED_FOLDER

# Ensure all folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPTED_FOLDER'], exist_ok=True)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return render_template('index.html', uploaded_file=file.filename)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    key = int(request.form['key'])
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    encrypted_img = encrypt_image(file_path, key)
    encrypted_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    encrypted_img.save(encrypted_path)
    return render_template('index.html', encrypted_file=filename)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = int(request.form['key'])
    filename = request.form['filename']
    file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    decrypted_img = decrypt_image(file_path, key)
    decrypted_path = os.path.join(app.config['DECRYPTED_FOLDER'], filename)
    decrypted_img.save(decrypted_path)
    return render_template('index.html', decrypted_file=f'decrypted_{filename}')


if __name__ == '__main__':
    app.run()
