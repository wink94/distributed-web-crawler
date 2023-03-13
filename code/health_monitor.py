import subprocess
import datetime, threading
import requests
import sys
from util import node_retry
from generate_urls import make_urls, get_random_url


def periodic_healthcheck(node_count):
    urls = make_urls(node_count)
    retry_nodes = []
    for i in range(node_count):
        try:
            r = requests.get(url=urls[i]+'/health')
            resp = r.json()
            print('health status :'+ resp.status)

        except:
            print('heathcheck failed for '+urls[i])
            retry_nodes.append(i)

    for i in retry_nodes:
        node_retry(3,i,node_count,)

    retry_nodes.clear()

    threading.Timer(30,periodic_healthcheck,args=node_count)

if __name__ == '__main__':
	try:
		number_of_nodes = int(sys.argv[1])
		periodic_healthcheck(number_of_nodes)
	except:
		print("health monitor failed")
		exit(0)




