from enum import Enum


class DispatchStatus(Enum):
    ver = '0.1'
    
    QUEUED = 'queued'
    RUNNING = 'running'
    DONE = 'done'
