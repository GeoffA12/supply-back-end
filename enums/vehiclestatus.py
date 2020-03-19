from enum import Enum


class VehicleStatus(Enum):
    ver = '0.2.0'
    
    ACTIVE = 1
    INACTIVE = 2
    MAINTENANCE = 3
    
    @classmethod
    def translate(cls, string):
        name = string.replace(' ', '').lower()
        if name == 'active':
            return cls.ACTIVE
        elif name == 'inactive':
            return cls.INACTIVE
        elif name == 'maintenance':
            return cls.MAINTENANCE
        else:
            return None
