import unittest
from unittest.mock import MagicMock, patch

class TestRPCWriteFile(unittest.TestCase):

    def setUp(self):
        from test.helpers import Config, Properties, Method

        self.Config = Config
        self.Properties = Properties
        self.Method = Method

        #from amqppublisher.lib.rpc import Command, Invoker, WriteRPCFile, ExecuteRPCCallback, processRPCresult
        import amqppublisher.lib.rpc 
        self.WriteRPCFile = amqppublisher.lib.rpc.WriteRPCFile

    def tearDown(self):
        del self.Config
        del self.Properties
        del self.WriteRPCFile

    def test_init(self):
        from uuid import uuid4
        targetfile = str(uuid4())
        config = self.Config(rpc_workdir="", rpc_targetfile=targetfile)
        properties = self.Properties(message_id="")
        body=None
        w1 = self.WriteRPCFile(config,properties,body)
        self.assertEqual(targetfile,str(w1))
            
    def test_write_rpc_result_file_workdir(self):
        from uuid import uuid4
        from io import BytesIO
        
        rpc_workdir="/tmp"
        message_id=uuid4()
        body=b"testdata"
        
        
        w1 = self.WriteRPCFile(
            self.Config(rpc_workdir=rpc_workdir),
            self.Properties(message_id=message_id),
            body,
        )

        self.assertEqual(rpc_workdir + "/" + str(message_id),str(w1))

        fd = BytesIO()
        w1.write_content(fd)
        self.assertEqual(body, fd.getvalue())

    @patch("os.remove",create=True)
    def test_undo(self,patched):
        from uuid import uuid4
        from io import StringIO

        # just a random string
        rpc_targetfile=str(uuid4())
        
        body=b"testdata"
        
        
        w1 = self.WriteRPCFile(
            self.Config(
                rpc_workdir="/tmp",
                rpc_targetfile=rpc_targetfile,
            ),
            self.Properties(),
            body,
        )
        w1.undo()
        patched.assert_called_once_with(rpc_targetfile)

class TestRPCCallback(unittest.TestCase):
    def setUp(self):
        from test.helpers import Config, Properties, Method

        self.Config = Config
        self.Properties = Properties
        self.Method = Method

        #from amqppublisher.lib.rpc import Command, Invoker, WriteRPCFile, ExecuteRPCCallback, processRPCresult
        import amqppublisher.lib.rpc 
        self.ExecuteRPCCallback = amqppublisher.lib.rpc.ExecuteRPCCallback

        
    def tearDown(self):
        del self.Config
        del self.Properties
        del self.Method
        del self.ExecuteRPCCallback

    
    def test_init(self):
        filename=None
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(),
            self.Method(),
            filename,
        )
        #self.assertEqual(targetfile,str(w1))

    def test_callback_create_command_check_method(self):
        from uuid import uuid4
        routing_key = str(uuid4())

        filename=None
        
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(),
            self.Method(routing_key=routing_key),
            filename,
        )

        self.assertListEqual(
            ["-r",routing_key],
            e1._createcallbackcommand(),
        )

    def test_callback_create_command_check_property(self):
        from uuid import uuid4
        correlation_id = str(uuid4())

        filename=None
        
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(correlation_id=correlation_id),
            self.Method(),
            filename,
        )
        #print(e1._createcallbackcommand())
        self.assertListEqual(
            ["-c",correlation_id],
            e1._createcallbackcommand(),
        )

    def test_callback_create_command_check_empty(self):
        from uuid import uuid4
        correlation_id = str(uuid4())

        filename=None
        
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(),
            self.Method(),
            filename,
        )

        self.assertListEqual(
            [],
            e1._createcallbackcommand(),
        )

    def test_callback_create_command_check_headers(self):
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(headers=headers),
            self.Method(),
            filename,
        )
        self.assertListEqual(
            [
                '-h', "a=" + str(headers['a']),
                '-h', "b=" + str(headers['b']),
            ],
            e1._createhdr(),
        )

    @patch("subprocess.check_output",create=True)
    def test_callback_commandexecution(self,patched):
        
        from uuid import uuid4
        headers = { 'a': str(uuid4()),
                    'b': str(uuid4()) }
                                     
        filename=None
        
        e1 = self.ExecuteRPCCallback(
            self.Config(),
            self.Properties(headers=headers),
            self.Method(),
            filename,
        )
        e1.execute()
        
        patched.assert_called()
        
