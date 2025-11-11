name = input("What is your name? ")
age = int(input("How old are you? "))

print(f"Hello, {name}! You are {age} years old.")

years_to_25 = 25 - age
future_year = 2025 + years_to_25
print(f"You will turn 25 in {years_to_25} years, which will be {future_year}.")

if age < 18:
    print("You are a minor.")
else:
    print("You are an adult.")
    