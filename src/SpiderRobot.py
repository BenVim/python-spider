# 获取页码列表，循环页码，创建Pagemanage对象处理页信息
import re
import threading
from queue import Queue

from src.Base import Base
from src.DetailsAnalysis import DetailsAnalysis
from src.PageManage import PageManage


class SpiderRobot(Base):
    maxconnections = None
    url = "http://shop.99114.com/list/area/101118101_1"
    file = None
    pageLinkList = []
    queue = None
    def init(self):
        # 初始化
        self.file = open('./url.log', 'a', encoding='UTF-8', errors='ignore')
        self.queue = Queue()
        self.maxconnections = 10
        bsObj = self.getBeautifulSoup(self.getHtml(self.url))
        self.filterPageLinkList(self.getAllLinks(bsObj))
        self.pageAnalysis()

    def filterPageLinkList(self, links):
        patten = re.compile(r'http://shop.99114.com/list/area/[0-9_]+')
        for link in links:
            math = patten.match(link)
            if math:
                self.pageLinkList.append(math.group())


    def pageAnalysis(self):
        for link in self.pageLinkList:
            pageManage = PageManage()
            pageManage.initData(self.file, self.queue)
            print('pageAnalysis:',link)
            pageManage.analysis(link)

        print('queue len:', self.queue.qsize())

        semlock = threading.BoundedSemaphore(self.maxconnections)
        for i in range(self.queue.qsize()):
            semlock.acquire()
            details = DetailsAnalysis()
            details.initData(self.queue.get(), semlock)
            details.start()