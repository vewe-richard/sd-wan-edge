import http.client, urllib.parse
import time
import xml.etree.ElementTree as ET
import subprocess
import json

class Poll():
    def http_post(self, ctlurl, opts_dict):
        params = urllib.parse.urlencode(opts_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/xml"}
        conn = http.client.HTTPConnection(self._config["sms"], port=self._config["smsport"])
        conn.request("POST", ctlurl, params, headers)
        response = conn.getresponse()
        #print(response.status, response.reason)
        data = response.read()
        #print(data.decode())
        conn.close()
        return data

    def loop(self):
        options = {"SN": self._config["sn"], "CMD": "poll"}
        self.parsexml(self.http_post("/north/", options).decode())
        pass

    def parsexml(self, resp):
        print(resp)
        root = ET.fromstring(resp)
        for x in root:
            if x.tag == "version":
                print(x.attrib)
                #TODO, for mandatory version, try to upgrade local git repository
            elif x.tag == "command":
                print(x.attrib["line"])
                self.execute(x.attrib["line"])
        pass

    def execute(self, command):
        print("try to execute: ", command)
        items = command.split()
        sp = subprocess.run(items, stderr = subprocess.PIPE)
        if sp.returncode != 0:
            options = {"SN": self._config["sn"], "CMD": "actionresult", "actionID": items[2], "result": sp.stderr.decode()}
            print(options)
            self.http_post("/north/", options)


    def run(self):
        while True:
            self.loop()
            break
            time.sleep(1)
        pass

    def loadconfig(self):
        with open('config.json') as json_file:
            self._config = json.load(json_file)
            print(self._config)


if __name__ == "__main__":
    poll = Poll()
    poll.loadconfig()
    poll.run()
