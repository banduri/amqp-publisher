import subprocess
import time
import uuid
import logging
import sys
from pika import BasicProperties

log = logging.getLogger(__name__)



def getEncoding(args):
    """
    """
    mime_type = "application/octet-stream"
    mime_encoding = "binary"
    
    if args.mimetype == "guess":
        try:

            # get the mimetype of the file 
            cmd = [args.fileprog,'-b','--mime',args.inputfile]
            result = subprocess.check_output(cmd)
            mime_type = result.split(";")[0].strip()
            mime_encoding = result.split("=")[1].strip()
        except:
            pass
    else:
        try:
            (mime_type,mime_encoding) = args.mimetype.split(",",maxsplit=1)
        except:
            pass

    return (mime_type,mime_encoding)

def parseAdditionalHeaders(args):
    headerdata={}
    if args.additional_field:
        
        for x in args.additional_field:
            try:
                (k,v) = x.split("=",1)
                headerdata[k]=v
        
            except Exception as e:
                logging.warning("could not add additional headers %s" %e)
    return headerdata


def getMessageProperties(args):
    (mime_type,mime_encoding) = getEncoding(args)

    return BasicProperties(
        delivery_mode = args.deliverymode,
        content_type = mime_type,
        content_encoding = mime_encoding,
        headers = parseAdditionalHeaders(args),
        priority = args.priority,
        correlation_id = args.correlation_id, 
        reply_to = args.reply_to,
        expiration = None, 
        message_id = str(uuid.uuid4()), # make a random uuid
        timestamp = int(time.time()),
        type = None, 
        user_id = args.userid,
        app_id = args.appid,
        cluster_id = args.cluster_id)
