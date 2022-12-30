# playing around with classes
# %%
class MyClass:
    ''' A Simple Example Class'''
    i = 12345

    def __init__(self):
        self.data = []

    def f(self):
        return 'hello world'

# %%
x = MyClass()
x.i
# %%
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
    
    def f(self):
        return 'hello world'

# %%
x = Complex(3,-4.5)

x.counter = 1 # data attribute 
print(x.__dict__) 

# %%
x.f() # method object
xf = x.f
print(xf)

# x.f() is exactly equivalent to MyClass.f(x)
# %%
class Dog:
    kind = 'canine'         # class variable shared by all instances
    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

# %% 
d = Dog('Fido')
print(d.kind)

# %% 
class Dog:
    tricks = []             # mistaken use of a class variable
    def __init__(self, name):
        self.name = name
        self.tricks = [] 
    def add_trick(self, trick):
        self.tricks.append(trick)

# %% 
d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
d.tricks

# %% On Self
# Often, the first argument of a method is called self. This is nothing more than a convention:
# the name self has absolutely no special meaning to Python.

# %%
# Okay to define a method (function) outside of the class definition

# Function defined outside the class
def f1(self, x, y):
    return min(x, x+y)

class C:
    f = f1

    def g(self):
        return 'hello world'

    h = g

x = C()
x.f(x=10,y=10)


# %% Methods may call other methods by using attributes of the self argument
class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)

# %% Inheritance
# i.e.
class DerivedClassName(modname.BaseClassName):
    None 

# %% Built-in functions with inheritance
# Use isinstance() to check an instance’s type: isinstance(obj, int) will be True only if obj.__class__ is int or some class derived from int.

# Use issubclass() to check class inheritance: issubclass(bool, int) is True since bool is a subclass of int. However, issubclass(float, int) is False since float is not a subclass of int.

# %% private variables
# a name prefixed with an underscore (e.g. _spam)
    # should be treated as a non-public part of the API, 
    # whether as a function, method or data member

# valid use-case for class-private members is to avoid clashes of names with subclasses
    # 'name mangling'
    #  Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore) is textually replaced with _classname__spam, where classname is the current class name with leading underscore(s) stripped.

class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)

# %% iterators
s = 'abc'
it = iter(s)
next(it)
next(it)
next(it)