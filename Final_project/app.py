from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

app = Flask(__name__)

# Fonction pour chiffrer une vidéo avec AES-128
def chiffrement_AES(video_path):
    key = get_random_bytes(16)  # Clé AES aléatoire de 128 bits
    cipher = AES.new(key, AES.MODE_ECB)  # Mode de chiffrement ECB

    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()
        # Ajout de remplissage pour l'alignement sur la taille du bloc
        padded_data = video_data + b"\0" * (AES.block_size - len(video_data) % AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

    with open(video_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    return key

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour la page de chiffrement
@app.route('/chiffrement', methods=['POST'])
def chiffrement_video():
    if 'video' not in request.files:
        return "Aucune vidéo sélectionnée"

    video = request.files['video']
    video_path = os.path.join('uploads', video.filename)
    video.save(video_path)

    key = chiffrement_AES(video_path)

    return render_template('chiffrement.html', video_path=video_path, key=key.hex())

if __name__ == '__main__':
    app.run(debug=True)