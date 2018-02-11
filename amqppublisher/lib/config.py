
import argparse
# for appid
import os
import socket
import pwd

from amqppublisher.lib.tools import RawTextDefaultsHelpFormatter

parser = argparse.ArgumentParser(description = 'Sende a file to amqp-host',
                                 fromfile_prefix_chars='@',
                                 formatter_class = RawTextDefaultsHelpFormatter,
                                 usage='%(prog)s [options] <inputfile>',
                                 epilog = """
Example:

./amqp-publisher -o amqp.example.com -U guest -P guest -y myvhost -x myexchange -r myroutingkey <data.json> 

./amqp-publisher --x509 -c foo.crt -k foo.key -a cacert.crt <data.json>

./amqp-publisher --rpc --rpc-callback /usr/local/sbin/callback.sh <data.json> 

./amqp-publisher @mydefaults.conf 

 
""")



##############################
# Connection-Options
##############################

conparser = parser.add_argument_group('Connection')
conparser.add_argument('-o', '--host', type=str,
                       help = 'host or ip of amqp-server', metavar='<host>',
                       default = 'amqp.example.net')

conparser.add_argument('--port', '-p', metavar='<int>', type=int, help = 'port to connect to',
                       default = 5671)

conparser.add_argument('-U', '--username', metavar='<account>',
                       type=str, 
                       help = 'Username to use for authentication',
                       default = "guest")

conparser.add_argument('-P', '--password', metavar='<password>',
                       type=str, 
                       help = 'Password to use for authentication',
                       default = "guest")

conparser.add_argument('--retry',type = int,
                       help = 'Maximum number of retry attempts to connect to the server',
                       metavar = '<count>', default = 3)

conparser.add_argument('--retrydelay', type = int,
                       help = 'Time to wait in seconds, before the next connection retry',
                       metavar = '<seconds>', default = 1)

conparser.add_argument('--sockettimeout', metavar='<seconds>', type = float,
                       help = 'TCP Socket timeout in seconds',
                       default = 0.25)

#################
# TLS-Options
#################
tlsparser = parser.add_argument_group('x509 options')

tlsparser.add_argument('--x509', help = "use x509-certs instead of username:password", action = "store_true")

tlsparser.add_argument('-c', type=str, dest='certfile', help = 'certificate to use', metavar='<certfile>',
                       default = '/etc/amqp/amqp.crt')

tlsparser.add_argument('-k', type=str, dest='keyfile', help = 'private key', metavar='<keyfile>',
                       default = '/etc/amqp/amqp.key')

tlsparser.add_argument('-a',type=str, dest='cacert', help = 'ca to verify server against', metavar='<cacertfile>',
                       default = '/etc/amqp/cacert.crt')

##############################
# RPC-Options
##############################

rpcparser = parser.add_argument_group('remote procedure calls (RPC)')

rpcparser.add_argument('--rpc', help = ( "Es wird von einem zweitem Dienst eine Antwort erwartet. "
                                      "Dieser zweite dienst antwortet dann direkt an eine tmp exlusive "
                                      "Queue. Die Nachricht die als Antwort verstanden wird, in eine "
                                      "tmp-datei geschrieben, und der Pfad nach stdout ausgegeben"),
                       action = "store_true")

rpcparser.add_argument('--rpc-timeout', type=int, default = 20, metavar='<seconds>',
                       help = 'wie lange warten wir auf eine Antwort (Sekunden)')

rpcparser.add_argument('--rpc-targetfile', type=str, default = None, metavar='<path>',
                       help = ( "In welche Datei die Antwort des RPC-Servers geschrieben "
                                "werden soll. Wird keine angegeben, erfolgt eine "
                                "Ausgabe auf STDOUT"))

rpcparser.add_argument('--rpc-callback', type=str, default = None, metavar='<path>',
                       help = ( "Soll nach dem erhalten der Nachricht ein Programm aufgerufen "
                                "werden?"))

rpcparser.add_argument('--rpc-callback-timeout', type=int, default = 20, metavar='<seconds>',
                       help = 'wie lange warten wir bis das callback Program sich beendet hat?')

rpcparser.add_argument('--rpc-workdir',  type=str, default = "/var/tmp", metavar='<directory>',
                       help = 'wenn ein callback aufgerufen werden soll, werden die Daten aus der Nachricht hier temporaer abgelegt')

rpcparser.add_argument('--rpc-nodelete', help = ( "Keep the temp file after processing "
                                                  "the callback. see manpage for details..."),
                       action = "store_true")





#################
# message options
#################
msgparser = parser.add_argument_group('message properties options')

msgparser.add_argument('-y', '--vhost', type=str, help = 'vhost in amqp-host', metavar='<vhost>',
                       default = '/')

msgparser.add_argument('-x', '--exchange', type=str, help = 'exchange to publish to. Use "" for empty exchange', metavar='<exchange>',
                       default = 'amq.topic')

msgparser.add_argument('-r', '--routingkey', type=str, help = 'routingkey for message', metavar='<routingkey>',
                       default = 'rk.default')

msgparser.add_argument('--deliverymode', '-m', type=int, choices = [1,2], help = '1 transient | 2 persistent',
                       metavar='<int>', default = 2)

msgparser.add_argument('--additional-field', '-f',type=str, metavar='key=value',
                       help = 'add additional key=value to header of msg. Can be called multible times',
                       default = [],
                       action="append")

msgparser.add_argument('--priority', '-i', type=int,metavar='<int>',
                       help = ( 'set a priority to the message. the lowest priority is 0, '
                                'which is the default. The max-priority is defined as a '
                                'property of the queue but cannot be larger then 255.'),
                       default = 0)

msgparser.add_argument('--appid', '-j',type=str, metavar='<str>',
                       help = ("sets the app_id property of the amqp-message. if environment "
                               "var APPID is specified it will be used"),
                       default = '$APPID:' + str(os.getenv("APPID")) +
                       ';hostname:' + socket.getfqdn() + 
                       ';user:' + pwd.getpwuid(os.getuid())[0] +
                       ';cwd:' + os.getcwd() +
                       ';pid:' + str(os.getpid()) + 
                       ';ppid:' + str(os.getppid()))

msgparser.add_argument('--userid', '-u', type=str,metavar='<str>',default = None,
                       help = ("Setzt die user_id Eigenschaft der Nachricht. Sie muss "
                               "identisch sein mit der user_id die zum authentifizieren "
                               "verwendet wird. E.g. der CN im Zertifikat. Oder None um "
                               "diesen Check auf dem Server nicht durchzufuehren."))
                    

msgparser.add_argument('--reply_to', '-R',type=str, help = 'sets the reply_to property of the amqp-message.',
                       metavar = '<str>', default = None)

msgparser.add_argument('--correlation_id', '-C', type=str,
                       metavar = '<str>', default = None,
                       help = 'sets the correlation_id property of the amqp-message.')

msgparser.add_argument('--cluster_id', '-V', type=str, help = 'sets the cluster_id property of the amqp-message.',
                       metavar = '<str>', default = socket.getfqdn())

msgparser.add_argument('--mimetype', '-M', type = str, help = 'Mimetype und encoding. Beispiel application/octet-stream,binary. Steht der Parameter auf guess wird das Programm file verwendet um das encoding zu bestimmen. Schlaegt das fehl ist der default application/octet-stream,binary',
                    metavar = '<str>', default = "guess")



#################
# Mail-Options
#################
mailparser = parser.add_argument_group('mail notifications')

rpcparser.add_argument('--mail', help = "send mail on critical errors", action = "store_true")

mailparser.add_argument('--mail-target', type=str,
                        help = 'send an email on critical errors', metavar='<To:>',
                        default = 'trouble@example.net')

mailparser.add_argument('--mail-source', type=str, help = 'frommail', metavar='<From:>',
                        default = "amqp@example.net")

mailparser.add_argument('--mail-subject', type=str, help = 'the subject of the mail',
                        default = "Amqp critical messages", metavar='<Subject:>')

mailparser.add_argument('--mail-host', type=str, help = 'where is the mailhost', metavar='<mailserver>',
                        default = 'smtp.example.net')

mailparser.add_argument('--mail-user', type=str, help = 'the username for authentication to mailserver', metavar='<account>')

mailparser.add_argument('--mail-pass', type=str, help = 'the password for authentication to mailserver', metavar='<password>')

#################
# logging-options
#################

logparser = parser.add_argument_group('logging options')
                    
logparser.add_argument('-d', '--debug', help = 'debugging everything. Applicationlog goes to logfile, pika to STDERR',
                       action="store_true")

logparser.add_argument('-v', '--verbose', help = 'be verbose', action="store_true")
logparser.add_argument('--version', action='version', version='%(prog)s 0.9')
#################
# Misc-Options
#################

miscparser = parser.add_argument_group('misc options')

miscparser.add_argument('-F', '--fileprog', metavar = '<path>', type = str, help = 'wo ist das gnu file zu finden um mit magick den mimetype zu bestimmen?',
                        default = "/usr/bin/file")


#################
# Mandatory arguments
#################

parser.add_argument('inputfile', type=str, help = 'which file to send')
