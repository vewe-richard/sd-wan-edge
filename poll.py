import http.client, urllib.parse
import time
import xml.etree.ElementTree as ET
import subprocess

class Poll():
    def http_post(self, ctlurl, opts_dict):
        params = urllib.parse.urlencode(opts_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/xml"}
        conn = http.client.HTTPConnection("127.0.0.1", port=5000)
        conn.request("POST", ctlurl, params, headers)
        response = conn.getresponse()
        #print(response.status, response.reason)
        data = response.read()
        #print(data.decode())
        conn.close()
        return data

    def loop(self):
        options = {"SN": "000000001", "CMD": "poll"}
        self.parsexml(self.http_post("/north/", options).decode())
        pass

    def parsexml(self, resp):
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
        subprocess.run(command.split())


    def run(self):
        while True:
            self.loop()
            break
            time.sleep(1)
        pass

if __name__ == "__main__":
    poll = Poll()
    poll.run()
