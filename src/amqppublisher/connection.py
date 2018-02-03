from pika import ConnectionParameters, BlockingConnection
from pika.credentials import ExternalCredentials, PlainCredentials
from ssl import CERT_REQUIRED
import logging
import sys

log = logging.getLogger(__name__)

class AMQPConnectionBorg:
    _shared_state = {}
    def __init__(self,args):
        self.__dict__ = self.__class__._shared_state

        if not 'ch' in dir():
            self.ch = None
        if not 'con' in dir():
            self.con = None

        if not 'config' in dir():
            self.config = args
        if not 'ssl_options' in dir():
            self.ssl_options = dict(
                certfile = self.config.certfile,
                keyfile = self.config.keyfile,
                ca_certs = self.config.cacert,
                cert_reqs = CERT_REQUIRED )
        if not 'parameters' in dir():
            if self.config.tls:
                self.parameters=ConnectionParameters(
                    host = self.config.host,
                    port = self.config.port,
                    virtual_host = self.config.vhost,
                    connection_attempts = self.config.retry,
                    retry_delay = self.config.retrydelay,
                    socket_timeout = self.config.sockettimeout,
                    credentials = ExternalCredentials(),
                    ssl = True,
                    ssl_options = self.ssl_options)
            else:
                self.parameters=ConnectionParameters(
                    host = self.config.host,
                    port = self.config.port,
                    virtual_host = self.config.vhost,
                    connection_attempts = self.config.retry,
                    retry_delay = self.config.retrydelay,
                    socket_timeout = self.config.sockettimeout,
                    credentials = PlainCredentials(username=self.config.username,
                                                   password=self.config.password),
                    ssl = True)

    def getConnection(self):
        """
        @result: returns a pika channel
        """
        
        if all([self.ch,self.con]):
            return (self.ch,self.con)

        try:
            self.con = BlockingConnection(self.parameters)
            self.ch = con.channel()
        except Exception as e:
            log.critical("could not connect to server with paramters: %s\n  last Exception: %s\n  Additional arguments:%s" %(self.parameters,e,self.config))
            sys.exit(1)

        return (ch,con)
