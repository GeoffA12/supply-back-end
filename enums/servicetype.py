from enum import Enum, auto


class ServiceType(Enum):
    ver = '0.2.1'

    DRYCLEANING = 1
    RX = auto()
    COFFEE = auto()
    EVENTS = auto()

    @classmethod
    def translate(cls, string):
        name = string.replace(' ', '').lower()
        if name == 'drycleaning':
            return cls.DRYCLEANING
        elif name == 'rx':
            return cls.RX
        elif name == 'coffee':
            return cls.COFFEE
        elif name == 'events':
            return cls.EVENTS
        else:
            raise ValueError('Cannot translate into enum')
