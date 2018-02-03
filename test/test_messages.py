import unittest
from unittest.mock import MagicMock
from collections import namedtuple

import amqppublisher.lib.messages


class TestEncodingMethods(unittest.TestCase):

    def setUp(self):
        self.ArgsClass = namedtuple("ArgsClass",["fileprog","inputfile","mimetype"])
        self.getEncoding = amqppublisher.lib.messages.getEncoding
        # disable logger
        amqppublisher.lib.messages.log.warning=MagicMock()

    def test_mimetype_option(self):
        args = self.ArgsClass("","","application/octet-stream,binary")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')

    def test_mimetype_default_on_fail(self):
        args = self.ArgsClass("","","application/octet-stream;foobar")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')

    def test_mimetype_default_while_fail_on_guess(self):
        args = self.ArgsClass("","foobar","guess")
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(mime_type, 'application/octet-stream')
        self.assertEqual(mime_encoding, 'binary')
        
class TestParseAdditionalHeaders(unittest.TestCase):

    def setUp(self):
        self.ArgsClass = namedtuple("ArgsClass",["additional_field"])
        self.parseAdditionalHeaders = amqppublisher.lib.messages.parseAdditionalHeaders
        # disable logger
        amqppublisher.lib.messages.log.warning=MagicMock()

    def test_headers_add(self):
        args = self.ArgsClass(additional_field = ['test1=a','test2=b','test3=c'])

        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(headers,{ 'test1': 'a',
                                       'test2': 'b',
                                       'test3': 'c'} )

    def test_headers_partly_fail(self):
        args = self.ArgsClass(additional_field = ['test1=a','fail','test3=c'])
        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(headers,{ 'test1': 'a',
                                       'test3': 'c'} )

    def test_headers_overwrite(self):
        args = self.ArgsClass(additional_field = ['test=a','test2=b','test=c'])
        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(headers,{ 'test': 'c',
                                       'test2': 'b'} )
        
        
if __name__ == '__main__':
    unittest.main()

