import os

def getIp():
    wlan_ip = os.popen("ifconfig wlan0 | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    eth_ip = os.popen("ifconfig eth0 | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    lo_ip = os.popen("ifconfig lo | head -n2 | grep inet | awk '{print$2}'").read().replace('\n', '')
    #print(wlan_ip, eth_ip, lo_ip)
    if wlan_ip != '':
        return wlan_ip
    elif eth_ip != '':
        return eth_ip
    else:
        return lo_ip

if __name__ == '__main__':
    print(getIp())