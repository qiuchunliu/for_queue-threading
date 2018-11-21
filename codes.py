
import re
# 匹配数据
import requests
# 获取网页
import os
# 创建文件夹
from queue import Queue
# 线程安全模块
# 队列，先进先出
# 针对多个函数对同一个全局变量进行读写的情况
import threading
# 多线程


class Prod(threading.Thread):
    # 继承的应用
    def __init__(self, pagequeue, imgqueue, *args, **kwargs):
        super(Prod, self).__init__(*args, **kwargs)
        self.page_queue = pagequeue
        self.img_queue = imgqueue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            ht = requests.get(url)
            ht.encoding = ht.apparent_encoding
            title = re.findall(r'none">(.*?)</p>', ht.text)
            src = re.findall('data-original="(.*?)" alt="', ht.text)
            num = len(src)
            for img_info in range(num):
                self.img_queue.put((title[img_info], src[img_info]))


class Cons(threading.Thread):
    def __init__(self, pagequeue, imgqueue, *args, **kwargs):
        super(Cons, self).__init__(*args, **kwargs)
        self.page_queue = pagequeue
        self.img_queue = imgqueue

    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            filename, imgurl = self.img_queue.get()
            with open('C:\\Users\\qiuchunliu\\Desktop\\temp\\{}'.format(filename+'.'+imgurl.split('.')[-1]), 'wb') \
                    as pic:
                pic.write(requests.get(imgurl).content)
                print('下载完 %s ' % filename)


os.mkdir('C:\\Users\\qiuchunliu\\Desktop\\temp')


page_queue = Queue(2)
img_queue = Queue(1000)
for i in range(1, 3):
    page_url = 'http://www.doutula.com/photo/list/?page={}'.format(i)
    page_queue.put(page_url)

for i in range(4):
    t = Prod(page_queue, img_queue)
    t.start()
for i in range(4):
    t = Cons(page_queue, img_queue)
    t.start()

