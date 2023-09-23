"""Caesar Cipher"""

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

print("Do you want to encrypt or decrypt")
prompt = input('Type (e) for encrypt or (d) for decrypt: ').lower()
if prompt == 'e':
    try:
        shift = int(input("Type a shift key between 0 and 25:"))
        if shift < 0 or shift > 25:
            print("Please input a shift number between 0 and 25")
        else:
            encrypted_text = ''
            text = input("What text do you want to encrypt:\n> ").upper()
            for letter in text:
                if letter.isalpha():
                    index = letters.index(letter)
                    new_index = index + shift
                    encrypted_text += letters[new_index]
                else:
                    encrypted_text += letter
            print(encrypted_text)
    except ValueError:
        print("Invalid shift value. Please only integers are allowed")
elif prompt == 'd':
    try:
        shift = int(input("Type a shift key between 0 and 25:"))
        if shift < 0 or shift > 25:
            print("Please input a shift number between 0 and 25")
        else:
            decrypted_text = ''
            text = input("What text do you want to decrypt:\n> ").upper()
            for letter in text:
                if letter.isalpha():
                    index = letters.index(letter)
                    new_index = index - shift
                    decrypted_text += letters[new_index]
                else:
                    decrypted_text += letter
            print(decrypted_text)
    except ValueError:
        print("Invalid shift value. Please only integers are allowed")
else:
    print("Invalid option")
