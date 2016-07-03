# coding:utf-8
import urllib
import urllib2
import re
import thread
import time

class QSBK:
    def __init__(self):
        self.pageIndex = 1  #页面索引
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' #用户代理
        self.headers ={'User-Agent': self.user_agent}  #把代理添加到headers
        self.stories = []   #存放内容
        self.enable = False  #存放程序是否运行变量

    def getPage(self,pageIndex):#通过索引获取页面
        try:
            url = 'http://www.qiushibaike.com/hot/page/'  + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')#通过代理请求页面--打开得到的页面并转化编码
            return pageCode
        #如果页面请求失败则发送原因
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"链接错误，原因：",e.reason
                return None
    #从索引页面中获取页面内容
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败。。。'
            return None
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        items = re.findall(pattern,pageCode)
    #设置页面储存
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pageStories
    #下载页面
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1
    #从下载的页面中获取内容
    def getoneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()   #用回车加载下一条段子
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u"第%d页\t发布人：%s\t 赞：%s\n%s" %(page,story[0],story[2],story[1]) #d%代表整数，s%代表字符串
    #如何开始？
    def start(self):
        print u"正在读取糗事百科，按回车键查看新段子，按Q退出"
        self.enable = True #程序可以运行
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getoneStory(pageStories,nowPage)

spider = QSBK()  #要爬什么
spider.start()   #怎么爬
