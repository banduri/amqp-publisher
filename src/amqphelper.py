#!/usr/bin/env python

import subprocess

# the subprocessing module of python 2.6 does not provide a check_output
# so we provide it here
def backward_check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return output

def pikaversioncheck():
    from distutils.version import StrictVersion
    import pika
    REQ_PIKA_VERSION="0.9.14"
    if StrictVersion(pika.__version__) < StrictVersion(REQ_PIKA_VERSION):
        print("at least pika version %s"%(REQ_PIKA_VERSION))
        sys.exit(2)
