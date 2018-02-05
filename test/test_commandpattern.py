import unittest
from unittest.mock import MagicMock, patch

class TestRPCCommand(unittest.TestCase):

    def setUp(self):

        import amqppublisher.lib.rpc 
        self.Command = amqppublisher.lib.rpc.Command

    def tearDown(self):
        del self.Command

    def test_notimplemented_exception_protocollclass(self):
        with self.assertRaises(NotImplementedError):
            c1 = self.Command()

class TestRPCInvoker(unittest.TestCase):

    def setUp(self):
        from collections import namedtuple
        import amqppublisher.lib.rpc 

        self.Invoker = amqppublisher.lib.rpc.Invoker

        
    def tearDown(self):
        del self.Invoker

    def test_init(self):
        i1 = self.Invoker()

    def test_add_command_to_invoker(self):
        i1 = self.Invoker()
        c1 = MagicMock(name="Command1")
        c2 = MagicMock(name="Command2")
        i1.add(c1)
        i1.add(c2)
        self.assertIs(i1.commands[0],c1)
        self.assertIs(i1.commands[1],c2)
        self.assertEqual(len(i1.commands),2)
        self.assertEqual(len(i1.undos),0)
        

    def test_add_undocommand_to_invoker(self):
        i1 = self.Invoker()
        c1 = MagicMock(name="Command1")
        c2 = MagicMock(name="Command2")
        i1.addundo(c1)
        i1.addundo(c2)
        self.assertIs(i1.undos[0],c1)
        self.assertIs(i1.undos[1],c2)
        self.assertEqual(len(i1.commands),0)
        self.assertEqual(len(i1.undos),2)
        
    def test_execute_command_list(self):
        i1 = self.Invoker()
        c1 = MagicMock(name="Command1")
        c2 = MagicMock(name="Command2")
        i1.add(c1)
        i1.add(c2)
        i1.do()
        c1.execute.assert_called_once_with()
        c2.execute.assert_called_once_with()
        c1.undo.assert_not_called()
        c2.undo.assert_not_called()

    def test_undo_command_list(self):
        i1 = self.Invoker()
        c1 = MagicMock(name="Command1")
        c2 = MagicMock(name="Command2")
        i1.addundo(c1)
        i1.addundo(c2)
        i1.undo()
        c1.undo.assert_called_once_with()
        c2.undo.assert_called_once_with()
        c1.execute.assert_not_called()
        c2.execute.assert_not_called()

