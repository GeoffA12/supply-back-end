vehicles = (
    (12, 'active', 'qw3256', 1, 'Toyota', 'V-9', 23.42, 42.12, None, None,),
    (23, 'active', 'gf9012', 2, 'Mercedes', 'V-9', 102.43, 231.12, None, None,),
    (34, 'active', 'qw3256', 2, 'Toyota', 'V-10', 12.51, 87.51, None, None,),
    (45, 'active', 'qw3256', 1, 'Toyota', 'V-8', 23.42, 124.31, None, None,),
    )

vehicleCols = ['vehicleid', 'status', 'licenseplate', 'fleetid', 'make', 'model',
               'current_lat', 'current_lon', 'last_heartbeat', 'date_added']

vehiclesDictList = []

for row in vehicles:
    d = {}
    for colName, colVal in zip(vehicleCols, row):
        d[colName] = colVal
    print(d)
    vehiclesDictList.append(d)

print()

for vehicleDict in vehiclesDictList:
    for k, v in vehicleDict.items():
        print(k, v)
    print()
