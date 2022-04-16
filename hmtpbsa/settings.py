import os
import re
import sys
import uuid
import shutil
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
DEFAULT_CONFIGURE_FILE = os.path.dirname(os.path.abspath(__file__))+ '/data/default.ini'

PBSA_PARAMETER_FILE = os.path.dirname(os.path.abspath(__file__))+ '/data/mmpbsa.in'

# base configure
GMXEXE='gmx'
MDPFILESDIR = os.path.dirname(os.path.abspath(__file__)) + '/simulation/mdp'


logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


gmx_MMPBSA='gmx_MMPBSA'
if 'AMBERHOME' not in os.environ:
    #os.environ['AMBERHOME'] = set_amber_home(gmx_MMPBSA)
    raise Exception("Not found variable AMBERHOME")

if 'OMP_NUM_THREADS' in os.environ:
    OMP_NUM_THREADS = os.environ['OMP_NUM_THREADS']
else:
    OMP_NUM_THREADS = 4

def obtain_MMPBSA_version():
    versionFile = '/tmp/' + uuid.uuid1().hex
    os.system('gmx_MMPBSA -v >%s 2>&1 '%versionFile)
    with open(versionFile) as fr:
        text = fr.read()
        p = re.compile('v(\d\.\d)\.\d', re.S)
        m = re.search(p, text)
    os.system('rm %s'%versionFile)
    if m:
        version = float(m.groups()[0])
    else:
        logging.error('Can not found gmx_MMPBSA version.')
        print(text)
        sys.exit(1)
    return version

PBSA_VERSION = 1.5  #obtain_MMPBSA_version()