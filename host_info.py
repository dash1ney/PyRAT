import socket
from requests import get


def get_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = get('http://api.ipify.org').text

    return hostname, local_ip, public_ip
