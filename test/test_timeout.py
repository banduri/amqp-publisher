import unittest
from unittest.mock import MagicMock, patch
from collections import namedtuple

import amqppublisher.lib.tools

#disable logger
@patch('amqppublisher.lib.messages.log.warning')
class TestEncodingMethods(unittest.TestCase):

    # how to test for exceptions?
    def test_mimetype_option(self,*args):
        args = self.ArgsClass("","","application/octet-stream,binary")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')
