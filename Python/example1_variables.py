# Example 1: Variables and Basic Data Types in Python

# 1. Variable assignment and basic data types
name = "John"               # String - text enclosed in quotes
age = 30                    # Integer - whole number
height = 5.9                # Float - decimal number
is_student = True           # Boolean - True or False

# 2. Printing variables and concatenation
print("Basic variable values:")
print("Name:", name)
print("Age:", age)
print("Height:", height, "feet")
print("Is student?", is_student)

# String concatenation (combining strings)
print("\nString concatenation:")
greeting = "Hello, " + name + "!"
print(greeting)

# Using f-strings (formatted strings) - a modern way to format strings
print(f"Hi {name}, you are {age} years old and {height} feet tall.")

# 3. Basic data type operations
print("\nBasic operations:")
# Numeric operations
sum_result = 10 + 5
difference = 10 - 5
product = 10 * 5
division = 10 / 5  # Returns a float
integer_division = 10 // 3  # Returns an integer (floor division)
remainder = 10 % 3  # Modulo - returns the remainder
power = 2 ** 3  # Exponentiation - 2 raised to the power of 3

print(f"Sum: 10 + 5 = {sum_result}")
print(f"Difference: 10 - 5 = {difference}")
print(f"Product: 10 * 5 = {product}")
print(f"Division: 10 / 5 = {division}")
print(f"Integer Division: 10 // 3 = {integer_division}")
print(f"Remainder: 10 % 3 = {remainder}")
print(f"Power: 2 ** 3 = {power}")

# 4. Type conversion
print("\nType conversion:")
num_string = "42"
num_int = int(num_string)  # Convert string to integer
print(f"'{num_string}' as an integer: {num_int}")
print(f"Type of num_string: {type(num_string)}")
print(f"Type of num_int: {type(num_int)}")

# Convert integer to string
back_to_string = str(num_int)
print(f"{num_int} as a string: '{back_to_string}'")
print(f"Type of back_to_string: {type(back_to_string)}")

# Run this file to see the output!