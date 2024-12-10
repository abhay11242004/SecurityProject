import random

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


def generate_key_stream(seed, length):
    """Generates a key stream of random numbers (0-255) based on a seed."""
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]

def custom_encrypt_xor(image_path, seed):
    """Encrypts an image using XOR with a per-pixel random key and permutation"""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    total_pixels = len(pixels)
    key_stream = generate_key_stream(seed, total_pixels * 3)  # 3 keys per pixel (R, G, B)

    # Randomly shuffle pixel positions using the seed
    random.seed(seed)
    shuffled_indices = list(range(total_pixels))
    random.shuffle(shuffled_indices)

    encrypted_pixels = [None] * total_pixels
    for i, idx in enumerate(shuffled_indices):
        r, g, b, o = pixels[idx]
        r_key = key_stream[i * 3]
        g_key = key_stream[i * 3 + 1]
        b_key = key_stream[i * 3 + 2]
        encrypted_pixels[i] = (
            r ^ r_key,
            g ^ g_key,
            b ^ b_key,
            o  # Do not modify alpha channel (or leave as is)
        )

    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)

    return encrypted_img, shuffled_indices


def custom_decrypt_xor(encrypted_image_path, seed, shuffled_indices):
    """Decrypts an image using XOR with a per-pixel random key and permutation reversal"""
    img = Image.open(encrypted_image_path)
    pixels = list(img.getdata())

    # Generate the same random key stream and permutation as in encryption
    total_pixels = len(pixels)
    key_stream = generate_key_stream(seed, total_pixels * 3)

    # Decrypt each pixel using the same key stream and reverse the shuffle
    decrypted_pixels = [None] * total_pixels
    for i, idx in enumerate(shuffled_indices):
        r, g, b, o = pixels[i]
        r_key = key_stream[i * 3]
        g_key = key_stream[i * 3 + 1]
        b_key = key_stream[i * 3 + 2]
        decrypted_pixels[idx] = (
            r ^ r_key,
            g ^ g_key,
            b ^ b_key,
            o  # Do not modify alpha channel (or leave as is)
        )

    # Create the decrypted image
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img


def rotate_bits(value, n):
    return ((value << n) & 0xFF) | (value >> abs(8 - n))


def reverse_rotate_bits(value, n):
    return ((value >> n) | (value << abs(8 - n))) & 0xFF


def encrypt_substitution(image_path, shift):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    encrypted_pixels = [
        (rotate_bits(p[0], shift), rotate_bits(p[1], shift), rotate_bits(p[2], shift)) for p in pixels
    ]
    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)
    return encrypted_img


def decrypt_substitution(encrypted_image_path, shift):
    img = Image.open(encrypted_image_path)
    pixels = list(img.getdata())
    decrypted_pixels = [
        (reverse_rotate_bits(p[0], shift), reverse_rotate_bits(p[1], shift), reverse_rotate_bits(p[2], shift)) for p in pixels
    ]
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    return decrypted_img

