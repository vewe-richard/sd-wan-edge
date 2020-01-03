import http.client, urllib.parse

class Utils():
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
