from urllib.request import urlopen

from bs4 import BeautifulSoup


class Base:

    def __init__(self):
        pass

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
