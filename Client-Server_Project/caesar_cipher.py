#CAESAR CIPHER CODE

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

# Define the encryption function
def encrypt(plain_text, shift_amt):
    cipher_text = ""
    for letter in plain_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amt) % 26
            new_letter = alphabet[new_position]
            cipher_text += new_letter
        else:
            cipher_text += letter  # If it's not in the alphabet, just add it as is
    print(f"The encoded text is {cipher_text}")

# Define the decryption function
def decrypt(cipher_text, shift_amt):
    plain_text = ""
    for letter in cipher_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position - shift_amt) % 26
            new_letter = alphabet[new_position]
            plain_text += new_letter
        else:
            plain_text += letter  # If it's not in the alphabet, just add it as is
    print(f"The decoded text is {plain_text}")

# Execute the correct function based on the direction
if direction.lower() == 'encode':
    encrypt(plain_text=text, shift_amt=shift)
elif direction.lower() == 'decode':
    decrypt(cipher_text=text, shift_amt=shift)
else:
    print("Please enter either 'encode' or 'decode'!")
