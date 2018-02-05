import unittest
from unittest.mock import MagicMock, patch

class TestRPCWriteFile(unittest.TestCase):

    def setUp(self):
        from collections import namedtuple
        self.Config = namedtuple("Config",["rpc_workdir","rpc_targetfile"])
        self.Properties = namedtuple("Properties",["message_id"])

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
        from io import StringIO
        
        rpc_workdir="/tmp"
        rpc_targetfile=None
        message_id=uuid4()
        body="testdata"
        
        config = self.Config(rpc_workdir=rpc_workdir, rpc_targetfile=rpc_targetfile)
        properties = self.Properties(message_id=message_id)
        
        w1 = self.WriteRPCFile(config,properties,body)
        self.assertEqual(rpc_workdir + "/" + str(message_id),str(w1))

        fd = StringIO()
        w1.write_content(fd)
        self.assertEqual(body, fd.getvalue())

    @patch("os.remove",create=True)
    def test_undo(self,patched):
        from uuid import uuid4
        from io import StringIO

        # just a random string
        rpc_targetfile=str(uuid4())
        
        config = self.Config(rpc_workdir="/tmp", rpc_targetfile=rpc_targetfile)
        properties = self.Properties(message_id=None)
        body="testdata"
        
        
        w1 = self.WriteRPCFile(config,properties,body)
        w1.undo()
        patched.assert_called_once_with(rpc_targetfile)

