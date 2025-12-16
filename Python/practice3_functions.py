# Practice Exercise 3: Functions and Error Handling

# Task 1: Basic Function Creation
# Create a function 'calculate_area' that calculates the area of a rectangle
# It should take width and height as parameters and return the area

# Your code here:
def calculate_area(width, height):
    # Add your code here
    pass  # Replace this with your code

# Test your function
print(f"Area of rectangle with width 5 and height 3: {calculate_area(5, 3)}")

# Task 2: Default Parameters
# Create a function 'create_profile' that takes name, age, and occupation
# Make occupation a default parameter with value "Student"
# The function should return a dictionary with these values

# Your code here:
def create_profile(name, age, occupation="Student"):
    # Add your code here
    pass  # Replace this with your code

# Test your function
profile1 = create_profile("Alice", 25, "Engineer")
profile2 = create_profile("Bob", 20)  # Using default occupation
print("Profile 1:", profile1)
print("Profile 2:", profile2)

# Task 3: Variable Arguments
# Create a function 'calculate_average' that can take any number of numeric arguments
# and returns their average

# Your code here:
def calculate_average(*args):
    # Add your code here
    pass  # Replace this with your code

# Test your function
print(f"Average of 2, 4, 6: {calculate_average(2, 4, 6)}")
print(f"Average of 10, 20, 30, 40, 50: {calculate_average(10, 20, 30, 40, 50)}")

# Task 4: Error Handling
# Create a function 'safe_divide' that takes two parameters and returns their division
# Use try-except to handle the case where the second parameter is zero
# Return "Cannot divide by zero" in that case

# Your code here:
def safe_divide(a, b):
    # Add your code here
    pass  # Replace this with your code

# Test your function
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")

# Task 5: File Handling with Error Handling
# Create a function 'read_file_safely' that takes a filename and returns its contents as a string
# Use try-except to handle the case where the file doesn't exist
# Return "File not found" in that case

# Your code here:
def read_file_safely(filename):
    # Add your code here
    pass  # Replace this with your code

# Test your function
print(read_file_safely("existing_file.txt"))  # This file probably doesn't exist
print(read_file_safely("practice3_functions.py"))  # This file should exist

# Task 6: Create a Calculator
# Create a function 'calculator' that takes two numbers and an operation
# The operation can be "add", "subtract", "multiply", or "divide"
# Return the result of the operation
# Use error handling to deal with invalid operations and division by zero

# Your code here:
def calculator(a, b, operation):
    # Add your code here
    pass  # Replace this with your code

# Test your function
operations = ["add", "subtract", "multiply", "divide", "invalid", "divide"]
a_values = [10, 20, 5, 15, 10, 10]
b_values = [5, 10, 2, 3, 2, 0]

for i in range(len(operations)):
    print(f"{a_values[i]} {operations[i]} {b_values[i]} = {calculator(a_values[i], b_values[i], operations[i])}")

# When you're done, run this file to see if your code works correctly!