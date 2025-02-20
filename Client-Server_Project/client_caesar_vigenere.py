import socket

# Get user input for cipher type, direction, text, and shift/key
cipher_type = input("Choose cipher type ('caesar' or 'vigenere'):\n").lower()
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()

# Based on cipher type, prompt for the correct additional input
if cipher_type == 'caesar':
    shift = input("Type the shift number:\n")
    request = f"{cipher_type},{direction},{text},{shift}"
elif cipher_type == 'vigenere':
    key = input("Type the key for Vigenère cipher:\n").lower()
    request = f"{cipher_type},{direction},{text},{key}"
else:
    print("Invalid cipher type. Please choose either 'caesar' or 'vigenere'.")
    exit()

# Set up the client socket to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

# Send the request to the server
client_socket.send(request.encode('utf-8'))

# Receive and print the response from the server
response = client_socket.recv(1024).decode('utf-8')
print(f"Response from server: {response}")

client_socket.close()  # Close the client connection

