vehicles = (
    (12, 'active', 'qw3256', 1, 'Toyota', 'V-9', 23.42, 42.12, None),
    (23, 'active', 'gf9012', 2, 'Mercedes', 'V-9', 102.43, 231.12, None),
    (34, 'active', 'qw3256', 2, 'Toyota', 'V-10', 12.51, 87.51, None),
    (45, 'active', 'qw3256', 1, 'Toyota', 'V-8', 23.42, 124.31, None)
    )

vehicleCols = ['status', 'licenseplate', 'fleetid', 'make', 'model',
               'current_lat', 'current_lon', 'last_heartbeat']
vids = [x[0] for x in vehicles]
attr = [list(x[1:]) for x in vehicles]

# print(vehicleCols)
# print(attr)
d = {}

for id in vids:
    key = f'VehicleID{id}'
    d[key] = {}
    for a in attr:
        for col, e in zip(vehicleCols, a):
            d[key][col] = e

print(d)

# for k, v in d.items():
#     for vk, vv in v.items():
#         print(k, vk, vv)
# infoNoID = dict(zip(vehicleCols, attr[0]))

# newdict = dict(zip(vids, infoNoID))

# print(vids)
# print(attr)

# print(infoNoID)

print()
# for entry, data in infoNoID.items():
#     print(entry, data)

# print(newdict)
