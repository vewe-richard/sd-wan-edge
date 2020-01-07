import http.client, urllib.parse
import  json

class Utils():
    __instance = None

    @staticmethod
    def getInstance():
        if Utils.__instance == None:
            Utils()
        return Utils.__instance

    def __init__(self):
        if Utils.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Utils.__instance = self
            self._config = None
            self.loadconfig()

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

    def loadconfig(self):
        with open('config.json') as json_file:
            self._config = json.load(json_file)
            print(self._config)