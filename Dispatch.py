from datetime import time

class Dispatch(object):
    ver = '0.0'

    def __init__(self, vid, oid, loc_0, loc_f, timeCreated, isDone = False):
        self.vid = vid
        self.oid = oid
        self.loc_0 = loc_0
        self.loc_f = loc_f
        self.timeCreated = timeCreated
        self.isDone = isDone

    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route

    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff

    def loc_0Address(self):
        print('human readable of start location')
        # do geocoding stuff with mapservice

    def loc_fAddress(self):
        print('human readable of end location')
        # do geocoding stuff with mapservice

    def _asdict(self):
        return self.__dict__

    def __repr__(self):
        return f'Dispatch({self.vid}, {self.oid}, {self.loc_0}, {self.loc_f}, {self.timeCreated}, {self.isDone})'

    def __str__(self):
        return f'''Vehicle ID: {self.vid}
Order ID: {self.oid}
Start Location: {self.loc_0}
End Location: {self.loc_f}
Time Order was Placed: {self.timeCreated}, 
Dispatch Fulfilled: {self.isDone}
'''

if __name__ == '__main__':
    dispatch1 = Dispatch(vid = 12345,
                         oid = 123,
                         loc_0= (23.42, 42.12),
                         loc_f= (45.12, 124.22),
                         timeCreated= time(5, 18, 21)
                         )
    print(dispatch1)
    for k, v in dispatch1._asdict().items():
        print(f'{k} --> {v}')

    dispatch1.isDone = True
    print()
    print(dispatch1)

print(''' Dispatch Record SQL Table
 ___________________________________________________________________________________________________
| (PK) vid  | (PK) oid  | loc_0_lon | loc_0_lat | loc_f_lon | loc_f_lat | timeCreated   | isDone    |
| bigint    | bigint    | bigfloat  | bigfloat  | bigfloat  | bigfloat  | DateTime      | boolean   |
|:---       |:---       |:---       |:---       |:---       |:---       |:---           |:---       |
| 12345     | 123       | 23.42     | 42.12     | 45.12     | 124.22    | 05:18:21      | False     |
| 12345     | 5421      | 98.12     | 198.64    | 151.214   | 125.41    | 15:43:12      | True      |
| 45145     | 653124    | 214.12    | 56.01     | 141.121   | 215.231   | 23:51:59      | False     |
| 12345     | 41231     | 123.12    | 32.12     | 1.42      | 12.12     | 13:13:34      | False     |
| 31512     | 674134    | 71.13     | 52.53     | 89.121    | 53.13     | 10:42:31      | True      |
| 31512     | 41512     | 134.142   | 231.91    | 151.31    | 240.12    | 09:23:01      | True      |
| ...       | ...       | ...       | ...       | ...       | ...       | ...           | ...       |
|___________|___________|___________|___________|___________|___________|_______________|___________|

''')