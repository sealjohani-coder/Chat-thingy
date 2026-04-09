import random
import hashlib
import os

def encode(message, key):
    salt = int.from_bytes(os.urandom(1), 'big')
    seed1 = int(hashlib.sha256((key + str(salt) + "msg").encode()).hexdigest(), 16)
    seed2 = int(hashlib.sha256((key + str(salt) + "noise").encode()).hexdigest(), 16)
    msg_rng = random.Random(seed1)
    noise_rng = random.Random(seed2)

    bits = [int(bit) for c in message for bit in format(ord(c), '08b')]
    encoded = [salt]
    for i in bits:
        if i == 0:
            encoded.append(msg_rng.randint(1, 1000) * 2)
        if i == 1:
            encoded.append(msg_rng.randint(1, 1000) * 2 + 1)
        noise_count = noise_rng.randint(1, 3)
        for _ in range(noise_count):
            encoded.append(noise_rng.randint(1, 9999))
    return str(encoded)

def decode(encoded_str, key):
    encoded = list(map(int, encoded_str.strip("[]").split(", ")))
    salt = encoded[0]
    encoded = encoded[1:]
    seed2 = int(hashlib.sha256((key + str(salt) + "noise").encode()).hexdigest(), 16)
    noise_rng = random.Random(seed2)

    bits = []
    idx = 0
    while idx < len(encoded):
        bits.append(encoded[idx] % 2)
        idx += 1
        noise_count = noise_rng.randint(1, 3)
        for _ in range(noise_count):
            noise_rng.randint(1, 9999)
        idx += noise_count

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)
