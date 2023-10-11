# linux_v2ray

# 说明 : 本脚本提供解析v2ray订阅链接下拉配置文件及更新策略文件.
        
# 参数 :
    1. config=配置文件缓存路径
    2. log_PATH=log存储路径
    3. v2ray_config=规则策略路径.
# Linux自动化更新订阅:
     - 输入crontab -e编辑定时任务
     - 模板: [cron表达式] [python路径] [脚本路径] > [输出日志路径]
     - 例子: 0 0 18 * * ? /usr/bin/python3.8 ~/v2ray.py > ~/auto.log
     - Arch系也可通过:[cron表达式] systemctl restart clash.service[需自行设置]设置定时任务.在更新订阅后重启Clash-linux
~~~
sudo python3 v2ray_d.py -h   #获取帮助
sudo python3 v2ray_d.py -d   #从网络拉取节点信息
sudo python3 v2ray_d.py -p   #刷新最新的网速
sudo python3 v2ray_d.py -c   #切换配置文件，参数为切换序号 
sudo python3 v2ray_d.py -l   #获取可切换的参数列表 
sudo python3 v2ray_d.py -g   #获取当前选择的节点信息
sudo python3 v2ray_d.py      #按顺序执行 -d -p -c
~~~
