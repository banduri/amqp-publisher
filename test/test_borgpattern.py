import unittest
from unittest.mock import MagicMock, patch


class TestBorgPattern(unittest.TestCase):

    def setUp(self):
        from collections import namedtuple

        self.ArgsClass = namedtuple("ArgsClass",["host","port",
                                                 "vhost","retry","retrydelay",
                                                 "sockettimeout","username","password",
                                                 "certfile","keyfile","cacert","x509" ])

        self.args = self.ArgsClass(host="test", port=34, vhost="/", retry=1,
                                   retrydelay=1,sockettimeout=0.25,username="test",password="test",
                                   certfile="", keyfile="", cacert="",x509=False )

        self.patches = [
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
        del self.ArgsClass
        del self.args

    def test_borgpattern_init_username(self):
        b1 = self.AMQPConnectionBorg(self.args)

    def test_borgpattern_init_x509(self):
        self.args = self.ArgsClass(host="test", port=34, vhost="/", retry=1,
                                   retrydelay=1,sockettimeout=0.25,username="test",password="test",
                                   certfile="", keyfile="", cacert="",x509=True )
        b1 = self.AMQPConnectionBorg(self.args)

    def test_borgpattern_two_objects_one_state(self):
        b1 = self.AMQPConnectionBorg(self.args)
        b2 = self.AMQPConnectionBorg(self.args)
        self.assertNotEqual(b1,b2)
        self.assertEqual(b1.__dict__,b2.__dict__)

