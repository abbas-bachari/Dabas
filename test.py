import inspect

class MyClass:
    pass
obj=MyClass()
print(inspect.isclass(MyClass))  # True
print(inspect.isclass((type)))  # False (زیرا این یک نمونه از کلاس است)

