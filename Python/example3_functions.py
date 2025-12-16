# Example 3: Functions and Basic Error Handling in Python

# 1. Basic Function Definition and Calling
print("BASIC FUNCTIONS:")

# Function with no parameters
def say_hello():
    """This is a docstring - used to document what the function does."""
    print("Hello, World!")

# Calling the function
say_hello()

# Function with parameters
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
greet("Bob")

# Function with default parameter value
def greet_with_time(name, time_of_day="day"):
    print(f"Good {time_of_day}, {name}!")

greet_with_time("Charlie")
greet_with_time("Diana", "evening")

# 2. Return Values
print("\nRETURN VALUES:")

# Function that returns a value
def add(a, b):
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")

# Function that returns multiple values
def get_name_parts(full_name):
    parts = full_name.split()
    first_name = parts[0]
    last_name = parts[-1] if len(parts) > 1 else ""
    return first_name, last_name

first, last = get_name_parts("John Smith")
print(f"First name: {first}, Last name: {last}")

# 3. Variable Scope
print("\nVARIABLE SCOPE:")

# Global variable
message = "Global message"

def show_message():
    # Local variable
    local_message = "Local message"
    print(f"Inside function - Local: {local_message}")
    print(f"Inside function - Global: {message}")

show_message()
print(f"Outside function - Global: {message}")
# print(f"Outside function - Local: {local_message}")  # This would cause an error

# Modifying global variables
count = 0

def increment():
    global count  # Declare that we want to use the global variable
    count += 1
    print(f"Count inside function: {count}")

increment()
print(f"Count outside function: {count}")

# 4. Basic Error Handling
print("\nERROR HANDLING:")

# Try-except block
try:
    # This will cause a ZeroDivisionError
    result = 10 / 0
    print(f"Result: {result}")  # This line won't execute
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")

# Handling specific exceptions
try:
    # This will cause an IndexError
    numbers = [1, 2, 3]
    print(f"Fourth number: {numbers[3]}")
except IndexError:
    print("Error: Index out of range!")

# Try-except-else-finally
try:
    number = int("42")  # This will succeed
    result = 100 / number
except ValueError:
    print("Error: Could not convert to integer!")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
else:
    # Executes if no exceptions were raised
    print(f"Conversion successful! Result: {result}")
finally:
    # Always executes, regardless of whether an exception occurred
    print("This always runs, no matter what!")

# Run this file to see the output!