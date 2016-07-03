# coding:utf-8
import urllib
import urllib2
import re


class Douban:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-agent':self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self,pageIndex):
        try:
            url = 'https://movie.douban.com/top250?start=' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"链接错误，原因:",e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败"
            return None
        pattern = re.compile('<span class="title">(.*?)</span>.*?<p class="">(.*?)</p>.*?v:average">(.*?)</span>',re.S)
        items = re.findall(pattern,pageCode)

        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getoneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u"第%d页\t电影名称：%s\t 评分 %s \n\n \t \t信息：%s\n" %(page,story[0],story[2],story[1])

    def start(self):
        print u'请按回车搜索最高评分电影'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getoneStory(pageStories,nowPage)

spider = Douban()
spider.start()

