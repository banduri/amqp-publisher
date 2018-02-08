import unittest
from unittest.mock import MagicMock, patch


#disable logger
@patch('amqppublisher.lib.messages.log.warning')
class TestEncodingMethods(unittest.TestCase):

    def setUp(self):
        from test.helpers import Config
        import amqppublisher.lib.messages
        self.Config = Config
        self.getEncoding = amqppublisher.lib.messages.getEncoding

    def test_mimetype_option(self,*args):
        args = self.Config(
            fileprog = "",
            inputfile = "",
            mimetype = "application/octet-stream,binary",
        )
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(
            mime_type,
            'application/octet-stream')
        
        self.assertEqual(
            mime_encoding,
            'binary')

    def test_mimetype_default_on_fail(self,*args):
        args = self.Config(
            fileprog = "",
            inputfile = "",
            mimetype = "application/octet-stream;foobar",
        )
        mime_type, mime_encoding = self.getEncoding(args)
        
        self.assertEqual(
            mime_type,
            'application/octet-stream')
        
        self.assertEqual(
            mime_encoding,
            'binary')

    def test_mimetype_default_while_fail_on_guess(self,*args):
        args = self.Config(
            fileprog = "",
            inputfile = "foobar",
            mimetype = "guess",
        )
        
        mime_type, mime_encoding = self.getEncoding(args)
        self.assertEqual(
            mime_type,
            'application/octet-stream')
        
        self.assertEqual(
            mime_encoding,
            'binary')

@patch('amqppublisher.lib.messages.log.warning')
class TestParseAdditionalHeaders(unittest.TestCase):

    def setUp(self):
        from test.helpers import Config

        import amqppublisher.lib.messages
        self.Config = Config
        self.parseAdditionalHeaders = amqppublisher.lib.messages.parseAdditionalHeaders

    def test_headers_add(self,*args):
        args = self.Config(
            additional_field = [
                'test1=a',
                'test2=b',
                'test3=c',
            ]
        )

        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(
            headers,
            {
                'test1': 'a',
                'test2': 'b',
                'test3': 'c',
            }
        )

    def test_headers_partly_fail(self,*args):
        args = self.Config(
            additional_field = [
                'test1=a',
                'fail',
                'test3=c',
            ]
        )

        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(
            headers,
            {
                'test1': 'a',
                'test3': 'c',
            }
        )

    def test_headers_overwrite(self,*args):
        args = self.Config(
            additional_field = [
                'test=a',
                'test2=b',
                'test=c',
            ],
        )
        headers = self.parseAdditionalHeaders(args)
        self.assertDictEqual(
            headers,
            {
                'test': 'c',
                'test2': 'b',
            }
        )


class TestMessagePropertie(unittest.TestCase):
    # since not using patch as a decorator, no *args is needed
    def setUp(self):

        self.patches = [
            patch('time.time',create=True,
                  new=MagicMock(return_value=1337)),
            patch('uuid.uuid4',create=True,
                  new=MagicMock(return_value='11111111-2222-3333-4444-555555555555')),
            patch('amqppublisher.lib.messages.parseAdditionalHeaders',
                  new=MagicMock(return_value={})),
            patch('amqppublisher.lib.messages.getEncoding',
                  new=MagicMock(return_value=("application/testdata-punk","text")))
        ]
        for x in self.patches:
            x.start()

        from test.helpers import Config
        import amqppublisher.lib.messages
        
        self.getMessageProperties = amqppublisher.lib.messages.getMessageProperties
        self.args = Config(
            deliverymode=123,
            priority=34,
            reply_to="testdata",
        )

    def tearDown(self):
        for x in self.patches:
            x.stop()
        
    def test_basicproperty_setup(self):
        from pika import BasicProperties

        props = self.getMessageProperties(self.args)

        self.assertEqual(
            props.delivery_mode,
            self.args.deliverymode)

        self.assertEqual(
            props.priority,
            self.args.priority)

        self.assertIsInstance(
            props,
            BasicProperties)

    def test_basicproperty_uuid(self):

        props = self.getMessageProperties(self.args)

        # from patching
        self.assertEqual(
            props.message_id,
            '11111111-2222-3333-4444-555555555555')

    def test_basicproperty_time(self):
        props = self.getMessageProperties(self.args)
        
        # from patching
        self.assertEqual(
            props.timestamp,
            1337)
        
    
if __name__ == '__main__':
    unittest.main()

