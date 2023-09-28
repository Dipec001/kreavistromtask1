import csv

## 1. Write a Python program that reads a text file and prints the number of lines, words, and characters in the file.

try:
    with open("test_write.txt") as t:
        data = t.read()

    print(f"Text file has {len(data.splitlines())} lines")

    words = data.split()
    print(f"Text file has {len(words)} words")
    print(f"Text file has {len(data)} characters")
except FileNotFoundError:
    print("File not found")

##2. Write a Python program that reads a CSV file and converts it into a dictionary.
# Each row of the CSV file should be a key-value pair in the dictionary.

csv_list = []
with open("weather_data.csv") as data_file:
    content = csv.reader(data_file)
    header = next(content)

    for row in content:
        csv_dict = {}
        csv_dict['day'] = row[0]
        csv_dict['temp'] = row[1]
        csv_dict['condition'] = row[2]

        csv_list.append(csv_dict)

for csv_dict in csv_list:
    print(csv_dict)


##3. Write a Python program that reads a binary file and converts it into a hexadecimal string.
# The program should output the hexadecimal string to a text file.

def binary_to_hexadecimal(input_file_path):
    """Function to read a binary file and convert it to a hexadecimal string"""
    try:
        with open(input_file_path, "rb") as binary_file:
            binary_data = binary_file.read()

            hexadecimal_string = binary_data.hex()

            return hexadecimal_string
    except FileNotFoundError:
        return "Error reading to the text file, please check file path and make sure it's correct"


def write_hexadecimal_to_text(hexadecimal_string, output_file_path):
    """Function to write a hexadecimal string to a text file"""
    try:
        with open(output_file_path, "w") as text_file:
            text_file.write(hexadecimal_string)
    except Exception as error:
        print("Error writing to the text file:", error)


input_file_path = "binary_file.bin"
output_file_path = "hexadecimal_output.txt"

hexadecimal_data = binary_to_hexadecimal(input_file_path)

write_hexadecimal_to_text(hexadecimal_data, output_file_path)
print(f"Hexadecimal data written to {output_file_path}")

## 4. Write a Python program that reads a text file containing numbers and calculates the sum of all the numbers in the file.

"""Assuming there's only a single number per line"""

numbers_sum = 0
try:
    with open("test4.txt", "r") as cal:
        for line in cal:
            numbers_sum += int(line)

        print(numbers_sum)
except FileNotFoundError:
    print("File not found. Please check file path specified and make sure a file with that name exists at the locatn")
except ValueError:
    print("There was an error converting a line to an integer. Make sure the file contains valid numbers.")

##5. Write a Python program that reads a text file and removes all the blank lines.
# The modified text should be written back to the file.

try:
    with open('test.txt', "r") as readfile:
        with open('test_write.txt', "w") as writefile:
            for line in readfile:
                if line.strip():
                    writefile.write(line)

    print(f"Blank lines removed. Result saved to 'test_write' file")

except FileNotFoundError:
    print(f"The 'test.txt' file does not exist.")
