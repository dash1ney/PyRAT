import json, cpuinfo, GPUtil, requests, socket
from platform import uname


def get_host_info():
    ipinfo = requests.get('http://ipinfo.io/json').json()
    gpus = GPUtil.getGPUs()

    data = {
        'public_ip': ipinfo['ip'],
        'local_ip': socket.gethostbyname(socket.gethostname()),
        'country': ipinfo['country'],
        'city': ipinfo['city'],
        'os': f'{uname().system} {uname().release} {uname().version}',
        'cpu': cpuinfo.get_cpu_info()['brand_raw'],
        'gpu': gpus[0].name if gpus else None
    }

    return json.dumps(data)