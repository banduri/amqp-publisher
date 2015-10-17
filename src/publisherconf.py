#!/usr/bin/env python

import pika
import argparse
from ssl import CERT_REQUIRED

parser = argparse.ArgumentParser(description = 'Sende a file to amqp-host',
                                 formatter_class = argparse.ArgumentDefaultsHelpFormatter,
                                 epilog = """
This ia a generic publisher. It sends the content of a file 
to an AMQP-Host.""")


parser.add_argument('-p', '--port', 
                    type=int, 
                    help = 'port to connect to',
                    default = 5673)

parser.add_argument('-o', '--host', 
                    type=str, 
                    help = 'host or ip of amqp-server',
                    default = 'localhost')

parser.add_argument('-l', '--retry', 
                    type=int, 
                    help = 'how many reconnects until failure',
                    default = 10)

parser.add_argument('-s', '--sleep', 
                    type=int, 
                    help = 'how many seconds to wait between two connections attempts',
                    default = 1)

parser.add_argument('-t', '--tls', 
                    help = 'enable for serverconnection',
                    action="store_true")

parser.add_argument('-a', '--cacert', 
                    type=str, 
                    help = 'only servers signed with this CAs are valid',
                    default = 'cacert.crt')

parser.add_argument('-U', '--username', 
                    type=str, 
                    help = 'Username to use for authentication',
                    default = "guest")

parser.add_argument('-P', '--password', 
                    type=str, 
                    help = 'Password to use for authentication',
                    default = "guest")

parser.add_argument('-x', '--x509CN', 
                    help = 'use a X509 amqp.crt for authentication',
                    action="store_true")

parser.add_argument('-C', '--certfile', 
                    type=str, 
                    help = 'client certificate to use',
                    default = 'amqp.crt')

parser.add_argument('-K', '--keyfile', 
                    type=str, 
                    help = 'client private key',
                    default = 'amqp.key')

parser.add_argument('-y', '--vhost', 
                    type=str, 
                    help = 'vhost in amqp-host')

parser.add_argument('-e', '--exchange', 
                    type=str, 
                    help = 'exchange to publish to')

parser.add_argument('-r', '--routingkey', 
                    type=str, 
                    help = 'routingkey for message')

parser.add_argument('-m', '--deliverymode', 
                    type=int, 
                    help = '1 transient | 2 persistent',
                    default = 2)

parser.add_argument('-M', '--mimetype', 
                    type=str, 
                    help = "the mimetype of the file to be send is based on the result of the unix-tool `file`. If no match is found, or `file` is not available, 'application/octet-stream' is used. With this parameter the mimetype can be forced to be a specific value.",
                    default = None)

parser.add_argument('-E', '--mimeencoding', 
                    type=str, 
                    help = "the mimeencoding of the file to be send is based on the result of the unix-tool `file`. If no match is found, or `file` is not available, 'binary' is used. With this parameter the mimeencoding can be forced to be a specific value."
                    default = None)

parser.add_argument('-f', '--additional-field', 
                    type=str, 
                    help = 'add additional key=value to header of msg. Can be called multible times',
                    default = [],
                    action="append")

parser.add_argument('-i', '--priority', 
                    type=str, 
                    help = 'set the priority in the amqpheader',
                    default = None)

parser.add_argument('-i', '--priority', 
                    type=int, 
                    help = 'set the priority in the amqpheader',
                    default = None)

parser.add_argument('-j', '--correlationid', 
                    type=str, 
                    help = 'set the correlation id in the amqpheader',
                    default = None)

parser.add_argument('-n', '--replyto', 
                    type=str, 
                    help = 'set the reply_to field in the amqpheader',
                    default = None)

parser.add_argument('-q', '--userid', 
                    type=str, 
                    help = 'set the userid field in the amqpheader',
                    default = None)

parser.add_argument('-w', '--appid', 
                    type=str, 
                    help = 'set the appid field in the amqpheader',
                    default = None)

parser.add_argument('-z', '--clusterid', 
                    type=str, 
                    help = 'set the clusterid field in the amqpheader',
                    default = None)



parser.add_argument('-v', '--verbose', 
                    help = 'be verbose',
                    action="store_true")

parser.add_argument('-d', '--debug', 
                    help = 'debugging everything. Applicationlog goes to logfile, pika to STDERR',
                    action="store_true")

parser.add_argument('inputfile', type=str, help = 'which file to send')

args = parser.parse_args()


ssl_options = dict(
                   certfile = args.certfile,
                   keyfile = args.keyfile,
                   ca_certs = args.cacert,
                   cert_reqs = CERT_REQUIRED )


creds=pika.credentials.ExternalCredentials()

parameters=pika.ConnectionParameters(
    host=args.host,
    port=args.port,
    virtual_host=args.vhost,
    credentials=creds,
    ssl=True,
    ssl_options=ssl_options)
