import os
import sys


#Command Protocoll
class Command:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def undo(self):
        pass

class Invoker:

    def __init__(self):
        self._commands = []
        self._undos = []

    @property
    def commands(self):
        return self._commands

    @property
    def undos(self):
        return self._undos
        
    def add(self, command):
        self._commands.append(command)

    def addundo(self,command):
        self._undos.append(command)
        
    def do(self):
        for c in self.commands:
            c.execute()

    def undo(self, filo=True):
        if filo:
            for c in reversed(self._undos):
                c.undo()
        else:
            for c in self._undos:
                c.undo()

class WriteRPCFile(Command):

    def __init__(self,config,properties,body):
        self.body = body
        self.rpc_targetfile = os.path.join(str(config.rpc_workdir), str(properties.message_id))
        if config.rpc_targetfile:
            self.rpc_targetfile = config.rpc_targetfile
    
    def execute(self):
        with open(self.rpc_targetfile, "wb") as fd:
            self.write_content(fd)

    def write_content(self,fd):
        fd.write(self.body)
        
    def undo(self):
        os.remove(self.rpc_targetfile)

    def __str__(self):
        return str(self.rpc_targetfile)

class ExecuteRPCCallback(Command):
    
    def __init__(self,config,properties,method,filename):
        self.filename = filename
        self.timeout = config.rpc_callback_timeout
        self.headers = properties.headers.items()
        self.commandarray = [
            config.rpc_callback, 
            "-r", str(method.routing_key),
            "-m", str(properties.content_type),
            "-e", str(properties.content_encoding),
            "-i", str(properties.message_id),
            "-p", str(properties.priority),
            "-d", str(properties.delivery_mode),
            "-c", str(properties.correlation_id),
            "-R", str(properties.reply_to),
            "-x", str(properties.expiration),
            "-y", str(properties.type),
            "-u", str(properties.user_id),
            "-a", str(properties.app_id),
            "-C", str(properties.cluster_id),
            "-t", str(properties.timestamp)]

    def execute(self):
        cmd = self.commandarray + self.headers
        cmd.extend(["-f", str(self.filename)])
        subprocess.check_output(cmd,timeout=self.timeout)

    def _createhdr(self):
        result = []
        if self.headers:
            for k,v in self.headers:
                result.append("-h")
                result.append("%s=%s" %(k,v))
        return result


def processRPCresult(method,properties,body,config):

    rpc_file = None
    invoker = Invoker()
    
    if any([config.rpc_targetfile, config.rpc_callback]):
        rpc_file = WriteRPCFile(config,properties,body)
        invoker.add(rpc_file)
        
        if not config.rpc_nodelete:
            invoker.addundo(rpc_file)
            
    else:
        # wir gehen einfach davon aus, dass es sich um utf8 handelt
        sys.stdout.write(str(body,'utf-8'))

    if config.rpc_callback:
        invoker.add(
            ExecuteRPCCallback(
                config,properties,method,rpc_file))
        

    invoker.do()
    invoker.undo()
