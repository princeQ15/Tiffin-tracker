fruits = ["apple", "banana", "cherry"]
print(fruits[0])
fruits.append("date")
fruits.insert(1, "blueberry")
print(fruits)

fruits.remove("banana")
last = fruits.pop()
print(last)

print(fruits[1:3])
