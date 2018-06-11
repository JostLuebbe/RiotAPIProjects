import requests as rq
import time
import xml.etree.ElementTree as ET
import json
import WinRateCalculator.json_to_xml as jtx


class RiotAPICall:
    def __init__(self, inc_call, inc_file_path):
        self.call = 'https://na1.api.riotgames.com' + inc_call
        self.key = '?api_key=RGAPI-049b8408-1f0f-442b-869a-1af09b8548c0'
        self.json_file = ''
        self.xml_root = ''
        self.file_path = inc_file_path

        try:
            self.make_call()
        except Exception as e:
            print('Unsuccessful Call')
            print(e)
        try:
            self.xml_root = jtx.convert_json_to_xml(self.json_file)
        except Exception as e:
            print('Unsuccessful XML Conversion')
            print(e)
        if self.file_path is not None:
            self.save_xml_file()

    def make_call(self):
        request = rq.get(self.call + self.key)
        if request.status_code == 200:
            print('Successful call for ' + self.file_path.split('/')[-1])
            self.json_file = request.json()
        elif request.status_code == 429:
            self.call_timeout(request.headers['Retry-After'])

    def call_timeout(self, inc_time):
        print('WE CALLED A TIMEOUT FOR ' + str(inc_time) + ' SECONDS!')
        time.sleep(int(inc_time))
        self.make_call()

    def save_xml_file(self):
        with open(self.file_path + '.xml', 'wb') as f:
            f.write(ET.tostring(self.xml_root))

    def save_json_file(self):
        with open(self.file_path + '.json', 'w') as f:
            json.dump(self.json_file, f, sort_keys=True, indent=4)

    def get_xml(self):
        return self.xml_root
