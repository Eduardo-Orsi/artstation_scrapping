from queue import Queue
import requests
from threading import Thread

QUEUE = Queue()

def get_proxies() -> list[str]:
    response = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc')
    if not response or response.status_code != 200:
        return
    
    response = response.json()["data"]
    for proxy in response:
        print(f"{proxy['ip']}:{proxy['port']}")
        QUEUE.put(f"{proxy['ip']}:{proxy['port']}")
    
    print('-------------------------------------------')
    

def verify_proxies():

    while not QUEUE.empty():
        proxy = QUEUE.get()

        try:
            response = requests.get(
                'http://ipinfo.io/json',
                proxies={"http": proxy,
                         "https": proxy},
                timeout=2
            )
        except:
            continue

        if response.status_code == 200:
            print(proxy)

        if QUEUE.empty():
            break

# get_proxies()

with open('Free_Proxy_List.txt', 'r') as file:
    proxies = file.read().split('\n')
    for proxy in proxies:
        QUEUE.put(proxy.strip())


threads = [Thread(target=verify_proxies) for _ in range(15)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print('finish')
    