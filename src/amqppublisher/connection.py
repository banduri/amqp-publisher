from pika import ConnectionParameters, BlockingConnection
from pika.credentials import ExternalCredentials, PlainCredentials
from ssl import CERT_REQUIRED
import logging
import sys

log = logging.getLogger(__name__)

def setupConnection(args):
    """
    @result: returns a pika channel
    """

    parameters=None
    ch = None

    ssl_options = dict(
        certfile = args.certfile,
        keyfile = args.keyfile,
        ca_certs = args.cacert,
        cert_reqs = CERT_REQUIRED )

    if args.tls:
        parameters=ConnectionParameters(
            host = args.host,
            port = args.port,
            virtual_host = args.vhost,
            connection_attempts = args.retry,
            retry_delay = args.retrydelay,
            socket_timeout = args.sockettimeout,
            credentials = ExternalCredentials(),
            ssl = True,
            ssl_options = ssl_options)
    else:
        parameters=ConnectionParameters(
            host = args.host,
            port = args.port,
            virtual_host = args.vhost,
            connection_attempts = args.retry,
            retry_delay = args.retrydelay,
            socket_timeout = args.sockettimeout,
            credentials = PlainCredentials(username=args.username,
                                           password=args.password),
            ssl = True)
    try:
        con=BlockingConnection(parameters)
        ch=con.channel()
    except Exception as e:
        log.critical("could not connect to server with paramters: %s\n  last Exception: %s\n  Additional arguments:%s" %(parameters,e,args))
        sys.exit(1)

    return ch
