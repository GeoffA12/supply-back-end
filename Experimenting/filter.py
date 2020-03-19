tuples = (
    (12345, 'active', 'qw3256', 1, 'Toyota', 'V-9', 23.42, 42.12, None),
    (13579, 'active', 'gf9012', 2, 'Mercedes', 'V-9', 102.43, 231.12, None),
    (12345, 'active', 'qw3256', 2, 'Toyota', 'V-10', 12.51, 87.51, None),
    (12345, 'active', 'qw3256', 1, 'Toyota', 'V-8', 23.42, 124.31, None)
    )

whitelist = ('V-9', 'V-8')

# newtuple = list(filter(lambda x: 'V-9' in x, tuples))
newtuple = [i for e in whitelist for i in tuples if e in i]
# print(newtuple)
for entry in newtuple:
    print(entry)

vehicles = [[x[3], x[0],
             f'{x[5]}: {x[6]}',
             f'Lat: {float(x[6])} Lon: {float(x[7])}',
             x[1], x[2], x[8]
             ] for x in newtuple]

for entry in vehicles:
    print(entry)
