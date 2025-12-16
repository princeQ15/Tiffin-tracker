# Example 2: Control Flow in Python (if statements and loops)

# 1. If-Elif-Else Statements
print("CONDITIONAL STATEMENTS:")
temperature = 75

# Simple if-else statement
if temperature > 80:
    print("It's hot outside!")
else:
    print("It's not too hot today.")

# If-elif-else chain
print("\nTemperature classification:")
if temperature < 40:
    print("It's cold!")
elif temperature < 65:
    print("It's cool.")
elif temperature < 85:
    print("It's warm.")
else:
    print("It's hot!")

# Logical operators: and, or, not
is_sunny = True
is_weekend = False

print("\nWeather and schedule check:")
if is_sunny and is_weekend:
    print("Perfect day for the beach!")
elif is_sunny and not is_weekend:
    print("Nice day, but you have to work.")
elif not is_sunny and is_weekend:
    print("You can relax, but indoors.")
else:
    print("Work day and bad weather.")

# 2. For Loops
print("\nFOR LOOPS:")

# Looping through a range of numbers
print("Counting from 1 to 5:")
for i in range(1, 6):  # range(start, stop) - stop is exclusive
    print(i, end=" ")  # end=" " keeps output on the same line
print()  # Print a newline

# Looping through a list
fruits = ["apple", "banana", "cherry", "date"]
print("\nFruit list:")
for fruit in fruits:
    print(f"- {fruit}")

# Looping with index using enumerate
print("\nFruits with indices:")
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# 3. While Loops
print("\nWHILE LOOPS:")

# Simple while loop
count = 5
print("Countdown:")
while count > 0:
    print(count, end=" ")
    count -= 1  # Decrement count by 1
print("\nBlast off!")

# While loop with break statement
print("\nLoop with break:")
number = 1
while True:  # Infinite loop
    if number > 5:
        break  # Exit the loop when number > 5
    print(number, end=" ")
    number += 1
print("\nBroke out of the loop")

# 4. Loop Control Statements
print("\nLOOP CONTROL:")

# Continue statement - skip the rest of the current iteration
print("Even numbers from 1 to 10:")
for i in range(1, 11):
    if i % 2 != 0:  # If i is odd
        continue    # Skip to the next iteration
    print(i, end=" ")
print()

# Nested loops
print("\nMultiplication table (1-3):")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} × {j} = {i*j}")
    print("-" * 10)  # Separator between rows

# Run this file to see the output!