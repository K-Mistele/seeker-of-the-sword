"""
>>> custom = open("custom_map.txt")
>>> var = []
>>> for line in custom:
...     var.append(list(line.strip("\n")))
...
>>> print var
  File "<stdin>", line 1
    print var
            ^
"""
