from PIL import Image
import random

def encrypt_image(image_path, key):
    """Encrypts an image by modifying pixel values."""
    img = Image.open(image_path)
    pixels = list(img.getdata())
    encrypted_pixels = [((p[0] + key) % 256, (p[1] + key) % 256, (p[2] + key) % 256) for p in pixels]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img

def decrypt_image(image_path, key):
    """Decrypts an image by reversing the encryption."""
    img = Image.open(image_path)
    pixels = list(img.getdata())
    decrypted_pixels = [((p[0] - key) % 256, (p[1] - key) % 256, (p[2] - key) % 256) for p in pixels]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img








def caesar_cipher_encrypt(img, key):
    """Encrypt image using Caesar Cipher."""
    pixels = list(img.getdata())
    encrypted_pixels = [((p[0] + key) % 256, (p[1] + key) % 256, (p[2] + key) % 256) for p in pixels]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img


def caesar_cipher_decrypt(img, key):
    """Decrypt image using Caesar Cipher."""
    pixels = list(img.getdata())
    decrypted_pixels = [((p[0] - key) % 256, (p[1] - key) % 256, (p[2] - key) % 256) for p in pixels]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img