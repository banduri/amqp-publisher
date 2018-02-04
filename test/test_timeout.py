import unittest
from unittest.mock import MagicMock, patch
from collections import namedtuple
from time import sleep

import amqppublisher.lib.tools 

class TestTimeoutHandling(unittest.TestCase):

    def setUp(self):
        self.Timeout = amqppublisher.lib.tools.Timeout
        self.TimeoutException = amqppublisher.lib.tools.TimeoutException
        self.maxTimeout = 1
    
    def test_timeout_init(self):
        
        timeout =  self.Timeout(self.maxTimeout)
        timeoutException = self.TimeoutException()

    def test_timeout_with(self):
        with self.Timeout(self.maxTimeout):
            pass

    def test_timeout_with_exit_reset(self):
        with self.Timeout(self.maxTimeout):
            pass
        sleep(self.maxTimeout+1)

    def test_timeout_exception_with(self):
        with self.assertRaises(self.TimeoutException):
            with self.Timeout(self.maxTimeout):
                sleep(self.maxTimeout + 1)

    def test_timeout_noexception_on_init(self):
        self.Timeout(self.maxTimeout)
        sleep(self.maxTimeout + 1)
