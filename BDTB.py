# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import re

class BDTB():


    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseUrl = baseUrl
        self.SeeLZ = "?see_LZ=" + str(seeLZ)   #初始化
        self.file = None
        self.floor = 1
        self.defaultTitle = u'badiudtieab'
        self.floorTag = floorTag


    def getPage(self,pageNum):#获取页面帖子
        try:
            url = self.baseUrl+ self.SeeLZ + "&pn="+str(pageNum)
            headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            request = urllib2.Request(url,headers=headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'connecting error:reason',e.reason
                return None


    def getTitle(self,page):
            pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>',re.S)
            result = re.search(pattern,page)
            if result:
                return result.group(1).strip()
                print result.group(1).strip()
            else:
                return None


    def getPageNum(self,page):
            pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
            result = re.search(pattern,page)
            if result:
                return result.group(1).strip()
            else:
                return None

    def getContent(self,page):
        pattern = re.compile('<div id="post_content.*?>(.*?)<',re.S)
        items = re.findall(pattern,page)
        contents =[]
        for item in items:
            contents.append(item.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title+ '.txt','w')
        else:
            self.file = open(self.defaultTitle + '.txt','w',encoding='utf-8')

    def writeData(self,contents):
        for item in contents:
            if self.floorTag =='1':
                floorLine = '\n' +str(self.floor) +u"----------------------------------" \
                                                   u"-------------------------------------" \
                                                   u"------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1



    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title =self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL is wrong'
            return
        try:
            print '该帖子共有'+ str(pageNum)+ '页'
            for i in range(1,int(pageNum)+1):
                print '正在写入第' +str(i)+'页'
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print '程序异常' + e.message
        finally:
            print '帖子信息爬取完成！'
print u'请输入子代号'
baseUrl = 'http://tieba.baidu.com/p/'+ str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言 ,是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")

bdtb = BDTB(baseUrl,seeLZ,floorTag)
bdtb.start()



