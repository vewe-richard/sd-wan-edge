import sys
from scripts.utils import Utils
import subprocess
import time

actionId = 0

def returnresult(actionid, result):
    options = {"SN": "00010001", "CMD": "actionresult", "actionID": actionid, "result": result}
    print(options)
    print(Utils().http_post("/north/", options))

def server(wan):
    print(wan)
    sp = subprocess.run(["ip", "tuntap", "del", "mode", "tun", "tun13"], stderr=subprocess.PIPE)
    sp = subprocess.run(["ip", "tuntap", "add", "mode", "tun", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, "ip tuntap: " + sp.stderr.decode())
        return
    sp = subprocess.run(["ip", "addr", "add", "10.10.0.1/24", "dev", "tun13"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, "ip addr:" + sp.stderr.decode())
        return
    sp = subprocess.run(["/home/richard/work/diyvpn/simpletun", "-i", "tun13", "-s", "-p", "5555", "-d"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, "simpletun:" + sp.stderr.decode())
        return
    else:
        sp.wait()


def client(wan, serverip):
    print(wan, serverip)
    sp = subprocess.run(["ip", "tuntap", "del", "mode", "tun", "tun13"], stderr=subprocess.PIPE)
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
    sp = subprocess.run(["ip", "route", "add", "172.16.117.0/24", "via", "10.10.0.1"], stderr=subprocess.PIPE)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    for i in range(0, 15):
        print("simpletun: " + str(i))
        sp = subprocess.run(["/home/richard/work/diyvpn/simpletun", "-i", "tun13", "-c", serverip, "-p", "5555", "-d"], stderr=subprocess.PIPE)
        if sp.returncode == 0:
            print("connect success")
            break
        else:
            print(sp.stderr.decode())
        time.sleep(1)
    if sp.returncode != 0:
        returnresult(actionID, sp.stderr.decode())
        return
    else:
        sp.wait()



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
