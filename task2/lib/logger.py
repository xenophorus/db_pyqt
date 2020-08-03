import logging
import sys
import time


if 'client.py' in str(sys.argv):
    log = logging.getLogger('client.app')
    logname = 'client'
else:
    log = logging.getLogger('server.app')
    logname = 'server'


fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

fhandler = logging.FileHandler(f'./log/{logname}_{time.strftime("%Y_%m_%d")}.log', encoding='utf-8')
fhandler.level = logging.DEBUG
fhandler.formatter = fmt

shandler = logging.StreamHandler(sys.stderr)
shandler.level = logging.DEBUG
shandler.formatter = fmt

log.addHandler(fhandler)
log.addHandler(shandler)
log.setLevel(logging.DEBUG)

log.info('logging started')
