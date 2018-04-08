# 根据页码链接，获取详情页链接列表,
# 遍历列表，每个链接创建一个DetailsAnalysis对象处理
import re
from queue import Queue

import pymysql

from src.Base import Base
from src.DetailsAnalysis import DetailsAnalysis


class PageManage(Base):
    companyLinkList = []
    file = None
    queue = None

    def __init__(self):
        super().__init__()

    def initData(self, file, queue):
        self.file = file
        self.queue = queue

    def analysis(self, link):
        self.companyLinkList = []
        bsObj = self.getBeautifulSoup(self.getHtml(link))
        self.filerLinks(self.getAllLinks(bsObj))
        #self.analysisWithLink(link)

    def filerLinks(self, links):
        patten = re.compile(r'http://shop.99114.com/\d+')
        for link in links:
            math = patten.match(link)
            if math:
                self.companyLinkList.append(math.group())
                self.queue.put(math.group())

    def analysisWithLink(self, page):
        for link in self.companyLinkList:
            self.openAndSave(link)



    def openAndSave(self, link):
        details = DetailsAnalysis()
        details.initData(link)
        details.start()
        print("analysisWithLink:", link)
