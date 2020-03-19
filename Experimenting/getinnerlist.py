l = [[1, 4],
     [2, 5],
     [3, 6],
     [4, 7],
     ]

found = [x for x in l if 1 in x]
print(found)
for entry in found:
    print(entry)
