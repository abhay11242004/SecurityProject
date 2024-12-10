from PIL import Image


def encrypt_caesar(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    encrypted_pixels = [((p[0] + key) % 256, (p[1] + key) % 256, (p[2] + key) % 256) for p in pixels]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img


def decrypt_caesar(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    decrypted_pixels = [((p[0] - key) % 256, (p[1] - key) % 256, (p[2] - key) % 256) for p in pixels]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img


def encrypt_vigenere(image_path, keyword):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    keyword_values = [ord(c) % 256 for c in keyword]
    encrypted_pixels = [
        (
            (p[0] + keyword_values[i % len(keyword_values)]) % 256,
            (p[1] + keyword_values[i % len(keyword_values)]) % 256,
            (p[2] + keyword_values[i % len(keyword_values)]) % 256
        )
        for i, p in enumerate(pixels)
    ]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img


def decrypt_vigenere(image_path, keyword):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    keyword_values = [ord(c) % 256 for c in keyword]
    decrypted_pixels = [
        (
            (p[0] - keyword_values[i % len(keyword_values)]) % 256,
            (p[1] - keyword_values[i % len(keyword_values)]) % 256,
            (p[2] - keyword_values[i % len(keyword_values)]) % 256
        )
        for i, p in enumerate(pixels)
    ]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img


def encrypt_xor(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    encrypted_pixels = [
        (
            p[0] ^ key,
            p[1] ^ key,
            p[2] ^ key
        )
        for p in pixels
    ]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img


def decrypt_xor(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    decrypted_pixels = [
        (
            p[0] ^ key,
            p[1] ^ key,
            p[2] ^ key
        )
        for p in pixels
    ]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img
