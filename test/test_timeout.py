import unittest
from unittest.mock import MagicMock, patch

class TestTimeoutHandling(unittest.TestCase):

    def setUp(self):
        import amqppublisher.lib.tools 

        self.Timeout = amqppublisher.lib.tools.Timeout
        self.TimeoutException = amqppublisher.lib.tools.TimeoutException
        self.maxTimeout = 1


    def tearDown(self):
        del self.Timeout
        del self.TimeoutException
        del self.maxTimeout
        
    def test_timeout_init(self):
        
        timeout =  self.Timeout(self.maxTimeout)
        timeoutException = self.TimeoutException()

    def test_timeout_with(self):
        with self.Timeout(self.maxTimeout):
            pass

    def test_timeout_with_exit_reset(self):
        from time import sleep
        with self.Timeout(self.maxTimeout):
            pass
        sleep(self.maxTimeout+1)

    def test_timeout_exception_with(self):
        from time import sleep
        with self.assertRaises(self.TimeoutException):
            with self.Timeout(self.maxTimeout):
                sleep(self.maxTimeout + 1)

    def test_timeout_noexception_on_init(self):
        from time import sleep
        self.Timeout(self.maxTimeout)
        sleep(self.maxTimeout + 1)
