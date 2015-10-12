# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re

#抓取美团网首页的服务链接
def getFirstPageUrls():
    firstpage = "http://cd.meituan.com/"
    html_file = openUrl(firstpage)
    soup = BeautifulSoup(html_file)
    deal_tiles = list(soup.find_all("h3","deal-tile__title"))
    hrefs = []
    for i in range(len(deal_tiles)):
        deal = str(deal_tiles[i].find("a",{"class":"w-link"})).replace("\n","")
        href = deal[deal.find("href"):deal.find("target")]
        hrefs.append(href)
    return hrefs

#根据url获取html文件
def openUrl(url):
    
    #根据url获取html文件
    url_response = urllib2.urlopen(url)
    html_file = url_response.read()
    return html_file

#根据url获取静态html文件进行内容解析
def htmlParser(url):

    #获取html内容
    html_file = openUrl(url)
    #将html文件转换为soup文件
    soup = BeautifulSoup(html_file)
    
    #定义需要的字段内容——此处的内容为html页面静态内容
    service_name = ""     #服务名称
    service_description = ""    #服务描述
    service_restrait = ""   #服务约束
    service_guarantee = ""  #服务保障

    #获取服务名称和服务描述信息
    headlines = soup.body.find_all("div","deal-component-headline")
    for headline in headlines:
        prefix = headline.find_all("span","deal-component-title-prefix")[0].getText().encode("utf-8")
        component = headline.find_all("h1","deal-component-title")[0].getText().encode("utf-8")
        description = headline.find_all("div","deal-component-description")[0].getText().encode("utf-8")
    service_name = prefix + component
    service_description = description


    #获取服务保障信息
    commitments = soup.body.find_all("div","deal-component-commitments")
    for commitment in commitments:
        anytime = commitment.find_all("a","anytime-money-back item")[0].getText().encode("utf-8")
        expiring = commitment.find_all("a","expiring-money-back item")[0].getText().encode("utf-8")
        instant = commitment.find_all("a","instant-money-back item")[0].getText().encode("utf-8")
    service_guarantee = "1." + anytime + ".\n2." + expiring + ".\n3." + instant + "."

    #获取服务约束信息
    deals = soup.body.find_all("div","deal-term")
    for deal in deals:
        purchaseinfo = deal.find_all("dl")[0]
        dts = list(purchaseinfo.find_all("dt"))
        dds = list(purchaseinfo.find_all("dd"))
        for i in range(1,len(dts)):
            temp = str(i) + "." + dts[i].getText().encode("utf-8") + ":" + dds[i].getText().encode("utf-8") + "\n"
            service_restrait += temp
    basic_info = "service_name:" + service_name + "\nservice_description:" + service_description + "\nservice_guarantee:" + service_guarantee + "\nservice_restrait:" + service_restrait
    return basic_info

#对html中根据js动态生成的内容进行解析
def jsParser(url):

    #构建需要返回评论信息的url
    home = url.split("/")[4]
    number = home.split(".")[0]
    rateUrl = "http://cd.meituan.com/deal/feedbacklist/" + str(number) + "/all/all/0/default/59?limit=10&showpoititle=0&offset=0"
    #定义需要的字段
    service_comments = ""     #服务评论

    #根据url获取html信息
    url_response = urllib2.urlopen(rateUrl)
    json_file = eval(url_response.read())
    html_file = json_file["data"]["ratelistHtml"].encode('utf-8')
    
    #对获取的html信息进行解析，获得对应标签的内容
    #获取服务评论信息
    soup = BeautifulSoup(html_file)
    contents = soup.find("p",{"class":"content"}).getText().encode("utf-8")
    contents = contents.replace("\n","").replace(" ","")

    #利用正则表达式来查找对应标签之间的评论信息
    #直接将返回的字符串（包含tag标签的内容）赋给service_comments
    service_comments = contents

    #将获取到的评论信息写入文件
    rate_info = "service_comments:" + service_comments
    return rate_info
    
#从url地址中解析出商品编号
def getServiceNo(url):
    #构建需要返回评论信息的url
    home = url.split("/")[4]
    number = home.split(".")[0]
    return number

if __name__ == "__main__":

    print "executing......"
    links = getFirstPageUrls()
    print len(links)
    for link in links:
        #对异常的服务进行处理
        try:
            temp = link.split("=")[1]
            url = temp[1:len(temp)-2]
            print url
            basic_info = htmlParser(url)
            rate_info = jsParser(url)
            file_number = getServiceNo(url)
            file_name = 'E:/result/' + file_number + '.txt'
            file_open = open(file_name,"w")
            file_open.writelines(basic_info + rate_info)
            file_open.close()
        except:
            print "failure to save some information"

    

    
    
    
