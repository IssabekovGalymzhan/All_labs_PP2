# Output Variables
x = "Python is awesome"
print(x) 
###
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)
###
x = 5
y = 10
print(x + y)
###
x = 5
y = "John"
print(x, y)

# Global Variables
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
###
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

# The global Keyword
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
###
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)