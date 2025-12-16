# Practice Exercise 2: Control Flow

# Task 1: If-Elif-Else Statements
# Write a function 'grade_calculator' that takes a score (0-100) and returns a letter grade
# A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: below 60
# Then test it with different scores

# Your code here:
def grade_calculator(score):
    # Add your code here
    pass  # Replace this with your code

# Test your function with these scores
test_scores = [95, 83, 75, 65, 55]
for score in test_scores:
    print(f"Score: {score}, Grade: {grade_calculator(score)}")

# Task 2: For Loops
# Create a function 'multiplication_table' that prints the multiplication table for a given number
# from 1 to 10
# Example: multiplication_table(5) should print:
# 5 x 1 = 5
# 5 x 2 = 10
# ...
# 5 x 10 = 50

# Your code here:
def multiplication_table(number):
    # Add your code here
    pass  # Replace this with your code

# Test your function
multiplication_table(7)

# Task 3: While Loops
# Create a simple guessing game function 'guess_number' where:
# - The function has a secret number (you can choose any number)
# - It asks the user to guess the number
# - If the guess is too high, it prints "Too high!"
# - If the guess is too low, it prints "Too low!"
# - If the guess is correct, it prints "Correct!" and ends
# - Limit the number of attempts to 5

# Your code here:
def guess_number():
    secret = 42  # You can change this to any number
    attempts = 0
    max_attempts = 5
    
    # Add your code here
    pass  # Replace this with your code

# Uncomment to test your function
# guess_number()

# Task 4: Nested Loops and Pattern Printing
# Create a function 'print_pattern' that takes a number n and prints a pattern like this (for n=5):
# *
# **
# ***
# ****
# *****

# Your code here:
def print_pattern(n):
    # Add your code here
    pass  # Replace this with your code

# Test your function
print_pattern(5)

# Task 5: List Comprehension (Advanced)
# Use list comprehension to create:
# - A list of squares of numbers from 1 to 10
# - A list of only even numbers from 1 to 20
# - A list of strings that are longer than 5 characters from a given list

# Your code here:
words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

squares = []  # List comprehension for squares
even_numbers = []  # List comprehension for even numbers
long_words = []  # List comprehension for words longer than 5 characters

print("Squares:", squares)
print("Even numbers:", even_numbers)
print("Long words:", long_words)

# When you're done, run this file to see if your code works correctly!