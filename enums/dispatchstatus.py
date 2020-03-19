from enum import Enum


class DispatchStatus(Enum):
    ver = '0.2.0'
    
    QUEUED = 1
    RUNNING = 2
    DONE = 3
    
    @classmethod
    def translate(cls, string):
        name = string.replace(' ', '').lower()
        if name == 'queued':
            return cls.QUEUED
        elif name == 'running':
            return cls.RUNNING
        elif name == 'done':
            return cls.DONE
        else:
            return None
