#!/usr/bin/env python

import sys
import subprocess

import logging
import sys
from pprint import pprint,pformat


from amqppublisher.lib.tools import Timeout, TimeoutException
from amqppublisher.lib.connection import AMQPConnectionBorg
from amqppublisher.lib.messages import getMessageProperties
from amqppublisher.lib.config import parser
from amqppublisher.lib.rpc import processRPCresult

log = logging.getLogger(__name__)

log_format_debug  = "%(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s"
log_format_normal = "%(asctime)s %(name) -30s %(levelname) -10s %(message)s"
log_format_normal = log_format_debug


logger = [ log,
           logging.getLogger('pika'),
           logging.getLogger('pika.callback'),
           logging.getLogger('pika.adapters.base_connection')]


def main(args):
  
    try:
        body = None

        with open(args.inputfile,"rb") as fd:
            body = fd.read()

        if args.rpc:
            (ch,con) = AMQPConnectionBorg(args).getConnection()
            result = ch.queue_declare(exclusive=True)
            args.reply_to = result.method.queue

        props = getMessageProperties(args)

        try:
            log.info("try to published Message (%d Bytes): %s" %(len(body),str(props)))
            
            (ch,con) = AMQPConnectionBorg(args).getConnection()

            ch.basic_publish(exchange=args.exchange,
                             routing_key=args.routingkey,
                             properties=props,
                             body=body)
            log.info("done: (%d Bytes): %s" %(len(body),str(props)))
        except Exception as e:
            log.critical("Exception: %s %s" %(type(e),str(e)))
            log.critical("could not published Message (%d Bytes): %s" %(len(body),str(props)))
            
        if args.rpc:

            if args.debug:
                print(args.reply_to)
            # nur an einer Nachricht interressiert, daher next auf das generatorobjekt
            try:
                (ch,con) = AMQPConnectionBorg(args).getConnection()
                ch.basic_qos(prefetch_count = 1)

                with Timeout(args.rpc_timeout):
                    (method, properties, body) = next(ch.consume(queue = reply_to))
                    processRPCresult(method, properties, body, args)
                    
                ch.basic_ack(delivery_tag = method.delivery_tag)
            except TimeoutException as e:
                raise(e)

    except TimeoutException as e:
        log.critical("Timeout beim warten auf die rpc-nachricht: \n Config:\n %s \n %s" %(pformat(args),pformat(e)))
        sys.exit(2)

    except Exception as e:
        log.critical("Could not send message \n Config:\n %s \n %s" %(pformat(args),pformat(e)))
        sys.exit(3)

    finally:

        # das hier wird 100% ausgefuehrt, auch wenn in dem exception handling vorher
        # schon ein sys.exit hinterlegt ist.

        if AMQPConnectionBorg(args).is_connected():
            (ch,con) = AMQPConnectionBorg(args).getConnection()
            ch.close()
            con.close()

    sys.exit(0)


def commandline():
    args = parser.parse_args(sys.argv)

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


    if args.debug:            
        logging.basicConfig(format=(log_format_debug))
    else:
        logging.basicConfig(format=(log_format_normal))

    for i in logger:
        if args.verbose:
            i.setLevel(logging.INFO)
        elif args.debug:
            i.setLevel(logging.DEBUG)
        else:
            i.setLevel(logging.ERROR)

    main(args)
    
    
if __name__ == "__main__":
    commandline()
