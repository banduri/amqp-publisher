import logging
import os
import socket
import pwd
from pika import ConnectionParameters
from pika.credentials import ExternalCredentials, PlainCredentials
from ssl import CERT_REQUIRED

from amqppublisher.config import parser


log_format_debug  = "%(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s"
log_format_normal = "%(asctime)s %(name) -30s %(levelname) -10s %(message)s"

args = parser.parse_args()


ssl_options = dict(
    certfile = args.certfile,
    keyfile = args.keyfile,
    ca_certs = args.cacert,
    cert_reqs = CERT_REQUIRED )


parameters=None
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

    

logger = [ logging.getLogger(__name__),
           logging.getLogger('pika'),
           logging.getLogger('pika.callback'),
           logging.getLogger('pika.adapters.base_connection')]

log = logger[0]

if args.mail:
    sh = logging.handlers.SMTPHandler(mailhost = args.mail_host,
                                      fromaddr = args.mail_source,
                                      toaddrs = [args.mail_target],
                                      subject = args.mail_subject,
                                      credentials = (args.mail_user,args.mail_pass),
                                      secure = (None, ))
    sh.setLevel(logging.ERROR)
    # wir senden nur unsere eigenen logmeldungen per mail
    # die von pika sind hier unerheblich / too much
    log.addHandler(sh)

logging.basicConfig()
for i in logger:
    if args.verbose:
        i.setLevel(logging.INFO)
    elif args.debug:
        i.setLevel(logging.DEBUG)
    else:
        i.setLevel(logging.ERROR)
        

if args.debug:            
    logging.basicConfig(format=(log_format_debug))
else:
    logging.basicConfig(format=(log_format_normal))
