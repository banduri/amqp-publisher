from typing import NamedTuple

class Config(NamedTuple):
    rpc_callback_timeout: int = 2
    rpc_callback: str = None
    rpc_workdir: str = None
    rpc_targetfile: str = None
    rpc_nodelete: bool = False
    host: str = "amqp.example.net"
    port: int = 5761
    vhost: str = "/"
    retry: int = 1
    retrydelay: int = 1
    sockettimeout: float = 0.25
    username: str = "guest"
    password: str = "guest"
    certfile: str = None
    keyfile: str = None
    cacert: str = None
    x509: bool = False
    fileprog: str = None
    inputfile: str = None
    mimetype: str = None
    additional_field: list = []
    deliverymode: int = 0
    priority: int = 0
    correlation_id: str = None
    reply_to: str = None
    userid: str = None
    appid: str = None
    cluster_id: str = None


class Properties(NamedTuple):
    message_id: str = None
    headers : dict = {}
    content_type: str = None
    content_encoding: str = None
    priority: int = 0
    delivery_mode: int = 0
    correlation_id: str = None
    reply_to: str = None
    expiration: str = None
    type: str = None
    user_id: str = None
    app_id: str = None
    cluster_id: str = None
    timestamp: int = 0

class Method(NamedTuple):
    routing_key: str = None
