import unittest
from unittest.mock import MagicMock, patch, call

class TestRPCProcessing(unittest.TestCase):
    def setUp(self):
        from test.helpers import Config, Properties, Method

        self.Config = Config
        self.Properties = Properties
        self.Method = Method

        self.mocks = {}
        self.patches = {
            'executeRPCCallback': patch('amqppublisher.lib.rpc.ExecuteRPCCallback'),
            'WriteRPCFile': patch("amqppublisher.lib.rpc.WriteRPCFile"),
            'Invoker': patch("amqppublisher.lib.rpc.Invoker"),
        }
        
        for k,v in self.patches.items():
            self.mocks[k] = v.start()

        #from amqppublisher.lib.rpc import Command, Invoker, WriteRPCFile, ExecuteRPCCallback, processRPCresult
        import amqppublisher.lib.rpc 
        self.processRPCresult = amqppublisher.lib.rpc.processRPCresult

    def tearDown(self):
        for k,v in self.patches.items():
            v.stop()
        del self.Config
        del self.Properties
        del self.Method
        del self.processRPCresult

    def test_rpc_no_processing(self):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config()
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        self.mocks['executeRPCCallback'].assert_not_called()
        self.mocks['WriteRPCFile'].assert_not_called()
        self.mocks['Invoker'].assert_called()

    def test_rpc_processing_writefile(self):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config(rpc_targetfile="/tmp/foobar")
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        self.mocks['executeRPCCallback'].assert_not_called()
        self.mocks['WriteRPCFile'].assert_called()
        self.mocks['Invoker'].assert_called()

    def test_rpc_processing_callback(self):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config(rpc_callback="/usr/sbin/randomprogram")
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        self.mocks['executeRPCCallback'].assert_called()
        self.mocks['WriteRPCFile'].assert_called()
        self.mocks['Invoker'].assert_called()

        expected_calls = [ call().do(), call().undo() ]
        self.mocks['Invoker'].assert_has_calls(expected_calls)
