import sys
from scripts.utils import Utils
import subprocess

actionId = 0

def returnresult(actionid, result):
    options = {"SN": "00010001", "CMD": "actionresult", "actionID": actionid, "result": result}
    print(options)
    print(Utils().http_post("/north/", options))

def server(wan):
    print(wan)
    sp = subprocess.run(["ip", "tuntap", "add", "mode", "tun", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    sp = subprocess.run(["ip", "addr", "add", "10.10.0.1/24", "dev", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    sp = subprocess.run(["/home/richard/work/diyvpn/simpletun", "-i", "tun13", "-s", "-p", "5555", "-d"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return



def client(wan, serverip):
    print(wan, serverip)
    sp = subprocess.run(["ip", "tuntap", "add", "mode", "tun", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    sp = subprocess.run(["ip", "addr", "add", "10.10.0.100/24", "dev", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    sp = subprocess.run(["ip", "link", "set", "tun13", "up"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    sp = subprocess.run(["/home/richard/work/diyvpn/simpletun", "-i", "tun13", "-c", serverip, "-p", "5555", "-d"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return



if __name__ == "__main__":
    print(sys.argv)
    actionID = sys.argv[1]
    try:
        if sys.argv[2] == "server":
            server(sys.argv[3])
        else:
            client(sys.argv[3], sys.argv[4])
    except Exception as e:
        returnresult(actionID, str(e))