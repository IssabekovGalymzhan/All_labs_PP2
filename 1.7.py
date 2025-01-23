# Upper Case
a = "Hello, World!"
print(a.upper())

# Lower Case
a = "Hello, World!"
print(a.lower())

# Remove Whitespace
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

# Replace String
a = "Hello, World!"
print(a.replace("H", "J"))

# Split String
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

# String Concatenation
a = "Hello"
b = "World"
c = a + b
print(c) 

a = "Hello"
b = "World"
c = a + " " + b
print(c)

# String Format
# F-Strings
age = 36
txt = f"My name is John, I am {age}"
print(txt)

# Placeholders and Modifiers
price = 59
txt = f"The price is {price} dollars"
print(txt)