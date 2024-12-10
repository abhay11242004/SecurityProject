from flask import Flask, render_template, request, redirect, url_for
import os
from ciphers import encrypt_caesar, encrypt_xor, decrypt_caesar,custom_encrypt_xor, \
    decrypt_xor, encrypt_substitution, decrypt_substitution, custom_decrypt_xor
from flask import send_from_directory
shuffled: [int]= []
app = Flask(__name__)
BASE_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ENCRYPTED_FOLDER = os.path.join(BASE_DIR, 'static', 'encrypted')
DECRYPTED_FOLDER = os.path.join(BASE_DIR, 'static', 'decrypted')

# Set Flask configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['DECRYPTED_FOLDER'] = DECRYPTED_FOLDER
app.config['Global'] = shuffled

# Ensure all folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPTED_FOLDER'], exist_ok=True)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/upload/encrypt', methods=['POST'])
def upload_encrypt():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return render_template('index.html', uploaded_encrypt_file=filename)


@app.route('/upload/decrypt', methods=['POST'])
def upload_decrypt():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    file.save(file_path)

    return render_template('index.html', uploaded_decrypt_file=filename)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    key = int(request.form['key'])
    cipher = request.form['cipher']
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if cipher == "caesar":
        encrypted_img = encrypt_caesar(file_path, key)
    elif cipher == "substitution":
        encrypted_img = encrypt_substitution(file_path, key)
    elif cipher == "xor":
        encrypted_img = encrypt_xor(file_path, key)
    elif cipher == "custom":
        encrypted_img, app.config["Global"] = custom_encrypt_xor(file_path, key)

    encrypted_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    encrypted_img.save(encrypted_path)
    return render_template('index.html', encrypted_file=filename)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = int(request.form['key'])
    cipher = request.form['cipher']
    filename = request.form['filename']
    file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)

    if cipher == "caesar":
        decrypted_img = decrypt_caesar(file_path, key)
    elif cipher == "substitution":
        decrypted_img = decrypt_substitution(file_path, key)
    elif cipher == "xor":
        decrypted_img = decrypt_xor(file_path, key)
    elif cipher == "custom":
        decrypted_img = custom_decrypt_xor(file_path, key, app.config["Global"])


    decrypted_path = os.path.join(app.config['DECRYPTED_FOLDER'], filename)
    decrypted_img.save(decrypted_path)
    return render_template('index.html', decrypted_file=filename)


@app.route('/static/encrypted/<filename>')
def download_encrypted(filename):
    return send_from_directory(app.config['ENCRYPTED_FOLDER'], filename, as_attachment=True)


@app.route('/static/decrypted/<filename>')
def download_decrypted(filename):
    return send_from_directory(app.config['DECRYPTED_FOLDER'], filename, as_attachment=True)



if __name__ == '__main__':
    app.run()
