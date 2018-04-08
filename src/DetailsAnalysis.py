import re
from threading import Thread
from urllib.request import urlopen

import pymysql
from bs4 import BeautifulSoup

from src.Base import Base


class DetailsAnalysis(Thread):
    db = pymysql
    mobile = None
    name = None
    companyName = None
    telephone = None
    address = None
    link = None
    semlock = None

    def __init__(self):
        super(DetailsAnalysis, self).__init__()

    def initData(self, link, semlock):
        self.link = link
        self.semlock = semlock
        self.db = pymysql.connect("localhost", "root", "root", "spider", use_unicode=True, charset="utf8")

    def run(self):
        self.analysis()

    def analysis(self):

        link = self.link
        bsObj = self.getBeautifulSoup(self.getHtml(link))
        self.mobile = self.getElementText(bsObj, 'span', {'class', 'phoneNumber'})
        self.name = self.getElementText(bsObj, 'span', {'class', 'name'})
        self.companyName = self.getElementText(bsObj, 'div', {'class', 'comIntroL'})
        self.telephone = self.getElementText(bsObj, 'span', {'class', 'telephoneShow'})
        self.address = self.getElementText(bsObj, '', {'id': 'detialAddr'})

        print(self.companyName, self.name, self.mobile, self.telephone, self.address)
        self.saveData()

    def getElementText(self, bsObj, element, obj):
        return self.getTextStr(bsObj.find(element, obj))

    def saveData(self):
        cursor = self.db.cursor()
        sql = "insert into company (company_name,name,mobile,phone,address) value ('" + self.companyName + "','" + self.name + "','" + self.mobile + "','" + self.telephone + "','" + self.address + "')"
        print("sql:",sql)
        cursor.execute(sql)
        self.db.commit()
        self.semlock.release()


    def saveUrl(self, link, page):
        patten = re.compile(r'http://shop.99114.com/(\d+)')
        math = patten.match(link)
        number = ""
        if math:
            numbers = math.groups()
            number = numbers[0]

        cursor = self.db.cursor()
        sql = "insert into address (url, number, page) values('"+link+"', "+ number +", '"+page+"')"
        cursor.execute(sql)
        self.db.commit()


    def getHtml(self, url):
        return urlopen(url)

    def getBeautifulSoup(self, htmlObj):
        return BeautifulSoup(htmlObj)

    def getAllLinks(self, bsObj):
        linkList = []
        for link in bsObj.findAll("a"):
            if 'href' in link.attrs:
                linkList.append(link.attrs['href'])

        return linkList

    def getTextStr(self, bsObj):
        if bsObj != None:
            str = bsObj.getText()
            str.replace("\n", "")
            str = str.strip()
            return str
        else:
            return "None"
