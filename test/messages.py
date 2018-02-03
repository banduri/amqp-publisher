import unittest
from collections import namedtuple

import amqppublisher.lib.messages


class TestEncodingMethods(unittest.TestCase):

    def setUp(self):
        self.ArgsClass = namedtuple("ArgsClass",["fileprog","inputfile","mimetype"])
        self.getEncoding = amqppublisher.lib.messages.getEncoding

    def test_message_type_option(self):

        args = self.ArgsClass("","","application/octet-stream,binary")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')

    def test_message_type_default_on_fail(self):
        args = self.ArgsClass("","","application/octet-stream;foobar")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')

    def test_message_type_fail_on_guess(self):
        args = self.ArgsClass("","foobar","guess")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')
        


        
if __name__ == '__main__':
    unittest.main()

