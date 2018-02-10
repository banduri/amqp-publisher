import unittest
from unittest.mock import MagicMock, patch


class TestBlockingConnection(MagicMock):
    def channel(*args,**kwargs):
        return "test-channel"


class TestConnection(unittest.TestCase):

    
    def setUp(self):
        from test.helpers import Config, Properties, Method

        self.args = Config()

        self.patches = [
            patch('pika.BlockingConnection', new=TestBlockingConnection),
            patch('pika.ConnectionParameters')
        ]
        for x in self.patches:
            x.start()
        import amqppublisher.lib.connection
        self.AMQPConnectionBorg = amqppublisher.lib.connection.AMQPConnectionBorg

    def tearDown(self):
        for x in self.patches:
            x.stop()
        del self.AMQPConnectionBorg
        del self.args

    def test_connection_notconnected(self):
        b1 = self.AMQPConnectionBorg(self.args)
        self.assertFalse(b1.is_connected())

    def test_getconnection(self):
        b1 = self.AMQPConnectionBorg(self.args)
        testchannel,con = b1.getConnection()
        self.assertEqual(testchannel,"test-channel")
        self.assertEqual(testchannel,con.channel())

            
    
