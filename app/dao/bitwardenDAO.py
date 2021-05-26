import json
import subprocess


class BitwardenDAO:
    SESSION = None

    def __init__(self, password=""):
        result = subprocess.run(['bw', 'unlock', password],
                                stdout=subprocess.PIPE)
        self.SESSION = str(result.stdout.split()[-1], 'utf-8')

    def get_item(self, topic):
        result = subprocess.run(['bw', 'get', 'item', topic, '--session', self.SESSION],
                                stdout=subprocess.PIPE)
        return json.loads(result.stdout)
