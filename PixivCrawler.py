# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os



class PixivCrawler(object):

    def __init__(self,id,password):
        #首先进行模拟登陆并保存会话状态---------------------------------------------------------------------------------------
        self.account = id  #账号
        self.password = password  #密码
        self.login_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'  # 登陆的URL
        self.post_url = 'https://accounts.pixiv.net/api/login?lang=zh'  # 提交POST请求的URL
        self.sessions = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'Origin': 'https://accounts.pixiv.net'
        }  # 用于模拟登陆时的头部参数
        self.page_login = self.sessions.get(url=self.login_url, headers=self.headers).content.decode('utf-8')  # 获取登录页面
        self.post_key = re.findall(re.compile('post_key" value="(.+?)"'), self.page_login)[0]  # 通过正则表达式提取post_key
        self.data = {
            'pixiv_id': self.account,
            'password': self.password,
            'captcha': '',
            'g_reaptcha_response': '',
            'post_key': self.post_key,
            'source': 'pc',
            'ref': 'wwwtop_accounts_indes',
            'return_to': 'https://www.pixiv.net/'
        }  #提交的参数
        self.sessions.post(self.post_url, data=self.data, headers=self.headers)  #提交表单进行登录
        self.cookies = self.sessions.cookies  # 获取cookies,这是必不可少的一步!
        #----------------------------------------------------------------------------------------------------------------

        self.list_img_url = []  #存入所有图片的URL

        self.id = input("请输入画师ID:")
        self.path = r"D:\Pixiv\%s" % self.id
        os.mkdir(self.path)
        os.chdir(self.path)

        self.collectImgUrl()
        self.imageDownload()
        self.page_total = 0

    def findHowManyPages(self):  #找出插画页数
        headers_selectedID = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'referer': 'https://www.pixiv.net/member_illust.php?id=%s' % self.id,
            'upgrade-insecure-requests': '1'}
        url = "https://www.pixiv.net/member_illust.php?id=%s&type=illust" % (self.id)
        html = self.sessions.get(url,headers = headers_selectedID)
        html = BeautifulSoup(html.text, "html.parser")
        chosen_page = html.find("ul", class_="page-list").find_all("li")
        self.page_total = int(chosen_page[len(chosen_page)-1].get_text())
        print("\n画师ID:%s\n插画一共有%d页" %(self.id,self.page_total))

    def isSinpleImg(self,each):  #判断多图或者单图
        each = str(each)
        pattern = re.compile("(?<=<div class=\"icon\"></div><span>)(.*)(?=</span></div>)")
        result = re.findall(pattern,each)
        if result:
            return int(result[0])
        else:
            return None


    def JPG_or_PNG(self,each):  #判断原图是JPG格式还是PNG格式
        headers_selectedImg = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'referer': 'https://www.pixiv.net/'}
        each = str(each)
        JPG = "_p0.jpg"
        PNG = "_p0.png"
        ERROR = "404 Not Found"
        pattern = re.compile("(?<=data-src=\")(.*)(?=\" data-tags=)")
        img_url = re.findall(pattern, each)[0]
        img_url = str(img_url)
        img_url = img_url.replace("/c/150x150/img-master/", "/img-original/")
        img_url = img_url.replace("_p0_master1200.jpg", "")  #先把原图的后缀去掉

        html_img = requests.get(img_url + PNG, headers=headers_selectedImg)  #假设原图的后缀是PNG
        if ERROR in str(html_img.content):
            img_url = img_url + JPG
            return img_url
        else:
            img_url = img_url + PNG
            return img_url



    def collectImgUrl(self):
        for page in range(1,4):
            page = str(page)

            headers_selectedID = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                'referer': 'https://www.pixiv.net/member_illust.php?id=%s' % self.id,
                'upgrade-insecure-requests': '1'}
            url = "https://www.pixiv.net/member_illust.php?id=%s&type=illust&p=%s" % (self.id,page)

            html = self.sessions.get(url, headers=headers_selectedID)
            html = BeautifulSoup(html.text, "html.parser")

            chosen_img_url = html.find_all("li", class_="image-item")

            for each in chosen_img_url:
                if self.isSinpleImg(each):  # 判断是不是多图
                    eachImg_number = self.isSinpleImg(each)  # 是多图
                    pattern = re.compile("(?<=data-src=\")(.*)(?=\" data-tags=)")
                    img_url = re.findall(pattern, str(each))[0]
                    img_url = img_url.replace("/c/150x150", "")
                    for i in range(eachImg_number):
                        temp_img_url = img_url.replace("p0", "p" + str(i))
                        self.list_img_url.append(temp_img_url)

                else:
                    self.list_img_url.append(self.JPG_or_PNG(each))


    def imageDownload(self):  #把所有图片的链接保存在文本文件中
        '''print("\n一共有%d张图片!开始下载!" % (len(self.list_img_url)))
        headers_selectedImg = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'referer': 'https://www.pixiv.net/'}

        for NO in range(0,len(self.list_img_url),1):
            try:
                with open(str(NO + 1) + ".jpg", "wb") as file:
                    image = requests.get(self.list_img_url[NO], headers=headers_selectedImg).content
                    file.write(image)
                    file.close()
                    print("正在下载第%d张图片:%s" % (NO + 1, self.list_img_url[NO]))
            except:
                print("下载失败!")
                NO -= 1'''

        with open(self.id + ".txt","a") as file:  #将图片URL保存在文本文件中.如果爬虫下载速度慢，可以在将URL复制到下载工具中去下载
            for each in self.list_img_url:
                file.write(each)
                file.write("\n")
        file.close()








p = PixivCrawler("SeekingMini@gmail.com","fzh981210")
input("请按任意键继续......")