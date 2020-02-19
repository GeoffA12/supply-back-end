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

    def getRoute(self, curLocation):
        print('my route')
        # do stuff to get the route

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
    print(dispatch1, '\n')
    for k, v in dispatch1._asdict().items():
        print(f'{k} --> {v}')

    dispatch1.isDone = True
    print(dispatch1, '\n')