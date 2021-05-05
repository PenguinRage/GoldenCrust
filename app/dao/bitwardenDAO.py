import json
import os
import subprocess


class BitwardenDAO:

    @staticmethod
    def get_item(topic):
        result = subprocess.run(['bw', 'get', 'item', topic, '--session', os.environ['BW_SESSION']], stdout=subprocess.PIPE)
        return json.loads(result.stdout)