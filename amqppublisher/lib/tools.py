import signal
import argparse

class TimeoutException(Exception):
    pass

class Timeout():
    """Timeout class using ALARM signal."""

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise TimeoutException()

# magic ward of oop
class RawTextDefaultsHelpFormatter(argparse.RawDescriptionHelpFormatter,argparse.ArgumentDefaultsHelpFormatter):
    pass
