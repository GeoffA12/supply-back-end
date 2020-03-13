tuple = (
    (0, 1),
    (2, 3),
    (4, 5),
    (6, 7),
    (8, 9)
    )

dict = dict(enumerate(x for x in tuple))
print(dict)
