import logging

FORMAT = '%(levelname)s: %(message)s'

logging.basicConfig(format=FORMAT)
log = logging.getLogger('todos')

def setLevel(level):
    log.setLevel(getattr(logging, level))
