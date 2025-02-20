import socket

# Alphabet for ciphers
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Caesar Cipher encryption
def caesar_encrypt(plain_text, shift_amt):
    cipher_text = ""
    for letter in plain_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amt) % 26
            new_letter = alphabet[new_position]
            cipher_text += new_letter
        else:
            cipher_text += letter  # Add non-alphabet characters as-is
    return cipher_text

# Caesar Cipher decryption
def caesar_decrypt(cipher_text, shift_amt):
    plain_text = ""
    for letter in cipher_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position - shift_amt) % 26
            new_letter = alphabet[new_position]
            plain_text += new_letter
        else:
            plain_text += letter  # Add non-alphabet characters as-is
    return plain_text

# Vigenère Cipher encryption
def vigenere_encrypt(plain_text, key):
    cipher_text = ""
    key_length = len(key)
    key_as_int = [alphabet.index(k) for k in key]
    plain_text_int = [alphabet.index(p) for p in plain_text if p in alphabet]
    
    for i in range(len(plain_text_int)):
        if plain_text[i] in alphabet:
            value = (plain_text_int[i] + key_as_int[i % key_length]) % 26
            cipher_text += alphabet[value]
        else:
            cipher_text += plain_text[i]  # Add non-alphabet characters as-is
    return cipher_text

# Vigenère Cipher decryption
def vigenere_decrypt(cipher_text, key):
    plain_text = ""
    key_length = len(key)
    key_as_int = [alphabet.index(k) for k in key]
    cipher_text_int = [alphabet.index(c) for c in cipher_text if c in alphabet]
    
    for i in range(len(cipher_text_int)):
        if cipher_text[i] in alphabet:
            value = (cipher_text_int[i] - key_as_int[i % key_length]) % 26
            plain_text += alphabet[value]
        else:
            plain_text += cipher_text[i]  # Add non-alphabet characters as-is
    return plain_text

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))  # Bind to localhost and port 9999
server_socket.listen(1)  # Server listens for one connection at a time
print("Server is listening on port 9999...")

while True:
    client_socket, addr = server_socket.accept()  # Accept incoming client connection
    print(f"Connection from {addr} has been established.")
    
    # Receive request from client (Format: "cipher_type,direction,text,shift/key")
    request = client_socket.recv(1024).decode('utf-8').split(',')
    
    cipher_type = request[0]  # Either 'caesar' or 'vigenere'
    direction = request[1]  # 'encode' or 'decode'
    text = request[2]
    
    if cipher_type == 'caesar':
        shift = int(request[3])  # Get the shift for Caesar Cipher
        
        if direction == 'encode':
            response = caesar_encrypt(text, shift)
        elif direction == 'decode':
            response = caesar_decrypt(text, shift)
        else:
            response = "Invalid operation for Caesar Cipher. Please send 'encode' or 'decode'."
    
    elif cipher_type == 'vigenere':
        key = request[3].lower()  # Get the key for Vigenère Cipher
        
        if direction == 'encode':
            response = vigenere_encrypt(text, key)
        elif direction == 'decode':
            response = vigenere_decrypt(text, key)
        else:
            response = "Invalid operation for Vigenère Cipher. Please send 'encode' or 'decode'."
    
    else:
        response = "Invalid cipher type. Please send 'caesar' or 'vigenere'."
    
    # Send the response back to the client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()  # Close the connection after responding
