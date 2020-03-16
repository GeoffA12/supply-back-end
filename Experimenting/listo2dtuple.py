list = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]
tuple = tuple((x,) for x in list)
print(tuple)
for i in tuple:
    print(i)
    print(type(i))
