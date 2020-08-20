from Crypto.Cipher import AES
from Crypto import Random
import re
from datetime import datetime
import random

def gen_key():
    in_key = b"Changemenowpleas"
    in_iv = b"changelatercools"
    today = datetime.utcnow().date()
    todaystr = today.strftime("%d/%m/%Y")
    todaystr += "fdsgd"
    todaystr.replace("f", "g")
    cipher = AES.new(in_key, AES.MODE_CFB, in_iv)
    key = cipher.encrypt(bytes(todaystr, 'utf-8'))
    return make_key_work(key)


def make_key_work(key):
    out = key
    while not len(out) - 16 == 0:
        if len(out) - 16 < 0:
            out += b'P' 
        elif len(out) - 16 > 0:
            out = out[:-1]
    return out


def sanitize(in_bytes):
    pattern = "'(.*?)'"
    out = re.search(pattern, str(in_bytes))
    return out.group(1)


def sanitize_double_quotes(in_bytes):
    pattern = '"(.*?)"'
    out = re.search(pattern, str(in_bytes))
    return out.group(1)


def encrypt(instring):
    key = gen_key()
    iv = Random.new().read(AES.block_size)
    print(len(iv))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = cipher.encrypt(bytes(instring, 'utf-8'))
    return iv + ciphertext


def decrypt(data):
    key = gen_key()
    outputcipher = AES.new(key, AES.MODE_CFB, data[0:16])
    plaintext = outputcipher.decrypt(data[16:])
    return sanitize(plaintext)

def encrypt_local(in_string):
    key = b'wELEBqwfR4wY1Nc8'
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = cipher.encrypt(bytes(in_string, 'utf-8'))
    return iv, encrypted


def decrypt_local(in_bytes):
    key = b'wELEBqwfR4wY1Nc8'
    cipher = AES.new(key, AES.MODE_CFB, in_bytes[0:16])
    output = cipher.decrypt(in_bytes[16:])
    return sanitize(output)


