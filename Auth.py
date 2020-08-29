#!/bin/python3
import socket
import json
import re
import encryption
import os
import random
from json import JSONEncoder

def gen_user_token(length):
    possible = 'abcdefghijklmnopqrstuvwxyzQWERTYUIOPLKJHGFDSAZXCVBNM<>.:|{}[]-_+1234567890!@#$%^&*()'
    return ''.join(random.choices(possible, k = length))

class User:
    def __init__(self, username, password, data=None):
        if data is None:
            self.name = username
            self.password = password
            self.token = None
        else:
            self.__dict__ = json.loads(data)

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def save_user(user, update=False):
    if update:
        if os.path.exists(f'{user.name}.user'):
            os.remove(f'{user.name}.user')
    elif update == False and os.path.exists(f'{user.name}.user'):
        return "Name Taken"
    f = open(f'{user.name}.user', 'wb+')
    instring = Encoder().encode(user)
    iv, to_save = encryption.encrypt_local(instring)
    f.write(iv)
    f.write(to_save)
    f.close()

def read_user(name):
    if os.path.exists(f'{name}.user'):
        f = open(f'{name}.user', 'rb')
        data = f.read()
        f.close()
        return User(None, None, data=encryption.decrypt_local(data))
    else:
        return None

def register(args):
    user = User(args[0], args[1])
    user.token = gen_user_token(256)
    result = save_user(user)
    if result is None:
        return f'{user.name}/{user.token}'
    else:
        return "UE"

def login(args):
    user = read_user(args[0])
    if user is not None:
        if args[1] == user.password:
            return f'{user.name}/{user.token}'
        else:
            return "IL"
    else:
        return "IL"

def RemoveNullTerminator(string):
    if '\\x00' in string:
        return string.replace('\\x00', '')
    else:
        return string

def verify(args):
    user = read_user(args[0])
    in_token = RemoveNullTerminator(args[1])
    print(in_token)
    if user is not None:
        if user.token == in_token:
            return "VT"
        else:
            if user.token == in_token[:-2]:
                return "VT"
            else:
                return "IT"
    else:
        return "IU"


def Test(args):
    return "Hello\r\n"

def sanitize(in_bytes):
	pattern = "'(.*?)'"
	out = re.search(pattern, str(in_bytes))
	out = out.group(1)
	return out


commands = {
    'L' : login,
    'R' : register,
    'V' : verify,
    'T' : Test,
}

def recv_all(conn):
    data = list()
    while True:
        data.append(conn.recv(2048))
        if not data[-1]:
            return b''.join(data)

TCP_IP = '192.168.86.39'
TCP_PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Server Started")
while True:
	conn, addr = s.accept()
	print(f'Connection established from {addr}')
	while True:
		data = conn.recv(BUFFER_SIZE)
		if not data:    break
		print("New Data")
		output = sanitize(data)
		try:
			if output.split("/")[3][:-2] == "JAVA":
				java = True
			else:
				java = False
		except IndexError:
			java = False
		print(java)
		command = output.split('/')[0]
		args = output.split('/')[1:]
		result = commands[command](args)
		print(result)
		if java:
			result = f'{result}\r\n'
		conn.send(bytes(result, "UTF-8"))
	conn.close()
	print(f"Connection to {addr} closed")
