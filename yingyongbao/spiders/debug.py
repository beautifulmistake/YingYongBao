"""
如何在单机上部署多个爬虫爬取一个网站
在spiders文件夹下创建debug.py文件
代码如下
需要注意的一些事项：
1、LOG_LEVEL 暂时不做修改，使用默认的DEBUG
2、8g内存，i5-8250的电脑可以开到55个进程，故第一次可以开启20个进程
"""
from scrapy.cmdline import execute
import os,sys
from time import sleep
from multiprocessing import Pool

sys.path.append(os.path.dirname(__file__))

def run_spider(number):
    print('spider %s is started ... ...' % number)
    # 执行启动爬虫的命令
    execute('scrapy runspider yingYongBaoSpider.py'.split(' '))  # 此处需要变更为你的爬虫名字

if __name__ == "__main__":
    p = Pool(3)    # 开启的进程数
    for i in range(3):
        # 创建进程
        p.apply_async(run_spider, args=(i,))
        sleep(2)
    p.close()
    p.join()
