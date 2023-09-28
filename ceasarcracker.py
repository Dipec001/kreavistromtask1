def caesar_cracker(ciphertext, shift):
    decrypted_text = ''
    for letter in ciphertext:
        if letter.isalpha():
            index = letters.index(letter.upper())
            new_index = (index - shift) % 26
            decrypted_text += letters[new_index]
        else:
            decrypted_text += letter
    return decrypted_text


# Letters for the Caesar cipher
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

encrypted_text = input("Enter the encrypted text: ").upper()

print("Brute-force decryption results:")
for shift in range(26):
    decrypted_result = caesar_cracker(encrypted_text, shift)
    print(f"Shift {shift}: {decrypted_result}")
