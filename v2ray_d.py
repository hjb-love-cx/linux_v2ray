
# 说明 : 本脚本提供解析v2ray订阅链接下拉配置文件及更新策略文件.
        
# 参数 :
#     1. config=配置文件缓存路径
#     2. log_PATH=log存储路径
#     3. v2ray_config=规则策略路径.
#     4. url=订阅链接地址
# Linux自动化更新订阅:
#     - 输入crontab -e编辑定时任务
#     - 模板: [cron表达式] [python路径] [脚本路径] > [输出日志路径]
#     - 例子: 0 0 18 * * ? /usr/bin/python3.8 ~/v2ray.py > ~/auto.log
#     - Arch系也可通过:[cron表达式] systemctl restart clash.service[需自行设置]设置定时任务.在更新订阅后重启Clash-linux

# 属性

import os
import sys
import yaml
import getopt
import datetime
import json
import base64
import urllib.request
import time
from ping3 import ping

opts, args = getopt.getopt(
    sys.argv[1:], '-h-p-c:-l-d-g', ['help', 'ping', 'change=', 'list', 'd', 'get'])

# encoding:utf-8
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
url = 123

v2ray_config = "./config.json"
log_PATH = "./v2ray.log"
config = "./123.conf"

# V2ray to Clash


def ping_host(ip):
    """
    获取节点的延迟的作用
    :param node:
    :return:
    """
    ip_address = ip
    response = ping(ip_address)
    if response is not None:
        delay = int(response * 1000)
        return delay


def log(msg):
    time = datetime.datetime.now()
    str = '['+time.strftime('%Y.%m.%d-%H:%M:%S')+']:'+msg 
    save_to_file(log_PATH, str)
    print(str)
# 保存到文件

def save_config(config_data, PATH):

    with open(PATH, mode='w', encoding='utf8') as r:

        json.dump(config_data, r, sort_keys=True, indent=4,
                  separators=(',', ':'), ensure_ascii=False)
    r.close

def save_to_file(file_name, contents):
    fh = open(file_name, 'a', encoding="utf-8")
    fh.write(contents + "\n")
    fh.close()
# 获取订阅地址数据:


def get_proxies(url):
    proxies = []
    # 请求订阅地址
    try:
        if (url == None):
            with open(config, 'r+', encoding='utf-8') as f:
                proxies = json.load(f)
                return proxies
        urllib.request.getproxies()
        urllib.request.ProxyHandler(proxies=None)
        req = urllib.request.Request(url=url, headers=headers)
        raw = urllib.request.urlopen(req).read().decode('utf-8')
        vmess_raw = base64.b64decode(raw)
        vmess_list = vmess_raw.splitlines()
        log('已获取'+str(len(vmess_list))+'个节点')
        # 解析vmess链接
    except:
        log("获取失败")
        with open(config, 'r+', encoding='utf-8') as f:
            proxies = json.load(f)
    else:
        for item in vmess_list:
            try:
                b64_proxy = item.decode('utf-8')[8:]
                proxy_str = base64.b64decode(b64_proxy).decode('utf-8')

            except:
                log('错误vmess' + str(item))
            else:
                proxies.append(json.loads(proxy_str))
        save_config(proxies, config)
    finally:
        return proxies

#加载信息到配置文件中
def load_local_config(proxy_raw, bit):

    with open(v2ray_config, 'rb') as fcc_file:

        fcc_data = json.load(fcc_file)
        for i in fcc_data["outbounds"]:
            try:
                for t in i["settings"]["vnext"]:
                    # print( str(t["port"]) + " -> " + proxy_raw["port"])
                    if bit == True:
                        return t["address"]
                    t["port"] = int(proxy_raw["port"])
                    t["address"] = proxy_raw["add"]
                    for e in t["users"]:
                        e["id"] = proxy_raw["id"]

            except:
                print("", end="")
        dist = fcc_data
    fcc_file.close
    save_config(dist, v2ray_config)
    time.sleep(1)
    os.system("systemctl restart v2ray")
    log("切换为：" + proxy_raw["ps"] + " 延时为：" + str(proxy_raw["ms"]))






#订阅列表测速
def curl_config(proxy_raw):
    num = 0
    ms_cp = 200
    json1 = []

    for i in range(len(proxy_raw)):

        url = proxy_raw[i]["add"]
        ms = ping_host(url)

        proxy_raw[i] = json.dumps(
            {**(proxy_raw[i]), **{"ms": ms}}, ensure_ascii=False)
        if ms != None and ms != 0:
            if int(ms) < ms_cp:
                ms_cp = int(ms)
                num = i
        proxy_raw[i] = json.loads(proxy_raw[i])
        log(proxy_raw[i]["ps"] + "的延迟为：" + str(ms) + "\t最低延迟:" + str(num))
        json1.append(proxy_raw[i])

    save_config(json1, config)
    return num

# 程序入口
def main():
    log("asdasd")
    proxy_raw = get_proxies(None)

    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("-h --help ")
            print("-d   从网络拉取节点信息")
            print("-p   刷新最新的网速")
            print("-c   切换配置文件，参数为切换序号 ")
            print("-l   获取可切换的参数列表 ")
            print("-g   获取当前选择的节点信息 ")
            exit()
        if opt_name in ('-d', '--d'):
            proxy_raw = get_proxies(url)
            exit()
        if opt_name in ('-p', '--ping'):
            curl_config(proxy_raw)
            exit()
        if opt_name in ('-c', '--change='):
            datapath = opt_value
            load_local_config(proxy_raw[int(datapath)], False)
            # do something
            exit()
        if opt_name in ('-l', '--datapath'):
            for i in range(len(proxy_raw)):
                print("序号：" + str(i) + " \t" +
                      proxy_raw[int(i)]["ps"] + "   \t延迟:" + str(proxy_raw[i]["ms"]))
            # do something
            exit()
        if opt_name in ('-g', '--get'):
            for i in range(len(proxy_raw)):
                if proxy_raw[int(i)]["add"] == load_local_config(proxy_raw, True):
                    print("当前选择：" + proxy_raw[int(i)]['ps'], end="\t")
                    print("延时为：" + str(ping_host(proxy_raw[int(i)]["add"]))+"ms")
            # do something
            exit()
    os.system("rm ./v2ray.log")
    proxy_raw = get_proxies(url)
    num = curl_config(proxy_raw)
    load_local_config(proxy_raw[num], False)


main()
