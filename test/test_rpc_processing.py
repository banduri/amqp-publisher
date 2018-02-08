import unittest
from unittest.mock import MagicMock, patch, call

class TestRPCProcessing(unittest.TestCase):
    def setUp(self):
        from test.helpers import Config, Properties, Method

        self.Config = Config
        self.Properties = Properties
        self.Method = Method

        #from amqppublisher.lib.rpc import Command, Invoker, WriteRPCFile, ExecuteRPCCallback, processRPCresult
        import amqppublisher.lib.rpc 
        self.processRPCresult = amqppublisher.lib.rpc.processRPCresult

    def tearDown(self):
        del self.Config
        del self.Properties
        del self.Method
        del self.processRPCresult

    @patch("amqppublisher.lib.rpc.ExecuteRPCCallback")
    @patch("amqppublisher.lib.rpc.WriteRPCFile")
    @patch("amqppublisher.lib.rpc.Invoker")
    def test_rpc_no_processing(self,p_invoker,p_writefile,p_callback):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config()
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        p_callback.assert_not_called()
        p_writefile.assert_not_called()
        p_invoker.assert_called()

    @patch("amqppublisher.lib.rpc.ExecuteRPCCallback")
    @patch("amqppublisher.lib.rpc.WriteRPCFile")
    @patch("amqppublisher.lib.rpc.Invoker")
    def test_rpc_processing_writefile(self,p_invoker,p_writefile,p_callback):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config(rpc_targetfile="/tmp/foobar")
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        p_callback.assert_not_called()
        p_writefile.assert_called()
        p_invoker.assert_called()

    @patch("amqppublisher.lib.rpc.ExecuteRPCCallback")
    @patch("amqppublisher.lib.rpc.WriteRPCFile")
    @patch("amqppublisher.lib.rpc.Invoker")
    def test_rpc_processing_callback(self, p_invoker, p_writefile, p_callback):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        config = self.Config(rpc_targetfile="/tmp/foobar")
        method = self.Method()
        properties = self.Properties(headers=headers)
        body = b"testdata"

        self.processRPCresult(method,properties,body,config)
        p_callback.assert_not_called()
        p_writefile.assert_called()
        p_invoker.assert_called()

        expected_calls = [ call().do(), call().undo() ]
        p_invoker.assert_has_calls(expected_calls)
