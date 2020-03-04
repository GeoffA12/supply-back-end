from enum import Enum

class status(Enum):
    ver = '0.1'

    QUEUED = 'queued'
    RUNNING = 'running'
    DONE = 'done'
