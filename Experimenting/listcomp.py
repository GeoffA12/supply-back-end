tup = (
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,),
    (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1,),
    (3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2,),
    (4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3,),
    (5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 4,),
    (6, 7, 8, 9, 10, 11, 1, 2, 3, 4, 5,),
    (7, 8, 9, 10, 11, 1, 2, 3, 4, 5, 6,),
    (8, 9, 10, 11, 1, 2, 3, 4, 5, 6, 7,),
    (9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8,),
    (10, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
    (11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,),
)
print(tup)

lst1 = [list(x)[0] for x in tup]
lst = [list(x)[2:4] + list(x)[6:10] for x in tup]
dct = dict(zip(lst1, lst))

dict2 = {}
for key, value in zip(lst1, lst):
    dict2[f'dispatch{key}'] = {
        'orderID': value[1],
        'custID': value[0],
        'dest': (value[2], value[3]),
        'timeOrderPlaced': value[4],
        'status': value[5]
    }

print(lst1)
print(lst)
print(dct)
print(dict2)