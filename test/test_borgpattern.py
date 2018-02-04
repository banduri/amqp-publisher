import unittest
from unittest.mock import MagicMock, patch
from collections import namedtuple
from pprint import pprint
import pika
import pika.credentials
import amqppublisher.lib.connection


class TestBorgPattern(unittest.TestCase):

    def setUp(self):

        
        self.ArgsClass = namedtuple("ArgsClass",["host","port",
                                                 "vhost","retry","retrydelay",
                                                 "sockettimeout","username","password",
                                                 "certfile","keyfile","cacert","x509" ])

        self.args = self.ArgsClass(host="test", port=34, vhost="/", retry=1,
                                   retrydelay=1,sockettimeout=0.25,username="test",password="test",
                                   certfile="", keyfile="", cacert="",x509=False )
        self.AMQPConnectionBorg = amqppublisher.lib.connection.AMQPConnectionBorg
    

    def test_borgpattern_init_username(self):
        b1 = self.AMQPConnectionBorg(self.args)

    def test_borgpattern_init_x509(self):
        self.args = self.ArgsClass(host="test", port=34, vhost="/", retry=1,
                                   retrydelay=1,sockettimeout=0.25,username="test",password="test",
                                   certfile="", keyfile="", cacert="",x509=True )
        b1 = self.AMQPConnectionBorg(self.args)

    def test_borgpattern_notconnected(self):
        b1 = self.AMQPConnectionBorg(self.args)
        self.assertFalse(b1.is_connected())

    def test_borgpattern_two_objects_one_state(self):
        b1 = self.AMQPConnectionBorg(self.args)
        b2 = self.AMQPConnectionBorg(self.args)
        self.assertNotEqual(b1,b2)
        self.assertEqual(b1.__dict__,b2.__dict__)

