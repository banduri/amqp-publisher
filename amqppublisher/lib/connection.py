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

        if not 'initDone' in self.__dict__:
            self.ch = None
            self.con = None
            self.config = args
            self.ssl_options = dict(
                certfile = self.config.certfile,
                keyfile = self.config.keyfile,
                ca_certs = self.config.cacert,
                cert_reqs = CERT_REQUIRED )
            if self.config.x509:
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
        self.initDone = True

    def is_connected(self):
        return all([
            self.con,self.ch,
            'initDone' in self.__dict__,
            'connectiontry' in self.__dict__
        ])
    
    def getConnection(self):
        """
        @result: returns a pika channel
        """
        if all([self.ch,self.con]):
                return (self.ch,self.con)

        if not 'connectiontry' in self.__dict__:
            try:
                self.con = BlockingConnection(self.parameters)
                self.ch = con.channel()
                return (self.ch,self.con)
            except Exception as e:
                log.critical("could not connect to server with paramters: %s\n  last Exception: %s\n  Additional arguments:%s" %(self.parameters,e,self.config))
                raise(e)
            finally:
                self.connectiontry = True

        return (None,None)
