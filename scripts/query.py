import json
import os
from scripts.utils import Utils
import subprocess

def getwans():
    sp = subprocess.run(["ip", "route", "show", "default"], stdout=subprocess.PIPE)
    wans = ""
    for line in sp.stdout.splitlines():
        l = line.decode().split()
#        wans += (l[4] + "," + l[2] + ";")
        sp2 = subprocess.run(["ip", "address", "show", l[4]], stdout=subprocess.PIPE)
        ip = None
        for ll in sp2.stdout.splitlines():
            nl = ll.decode()
            if "inet " in nl:
                ip = nl.split()[1].split("/")[0]
                break
        if ip != None:
            wans += (l[4] + "," + ip + ";")

    return wans

if __name__ == "__main__":
    with open('config.json') as json_file:
        config = json.load(json_file)
        config["CMD"] = "query"
        config["wans"] = getwans()
        print(Utils.getInstance().http_post("/north/", config))
        print(config)
