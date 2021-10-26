from abc import *
import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver

from urllib.request import urlopen
import ssl


class Crawler:
    def __init__(self, url, urls, atag, date):
        self.soup = None
        self.arr = []
        self.url = url
        self.setSoup(url)
        self.urls = self.soup.select(urls)
        self.atag = self.soup.select(atag)
        self.date = self.soup.select(date)
        self.dateMatcher = {
            "Jan" : "01",
            "Feb" : "02",
            "Mar" : "03",
            "Apr" : "04",
            "May" : "05",
            "Jun" : "06",
            "Jul" : "07",
            "Aug" : "08",
            "Sep" : "09",
            "Oct" : "10",
            "Nov" : "11",
            "Dec" : "12"
        }

    def setSoup(self, url):
        try:
            context = ssl._create_unverified_context()
            html = urlopen(url, context=context).read()
        except:        
            res = requests.get(url)
            html = res.content

        self.soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')


    def getSoup(self):
        return self.soup

        
    def dayFarmat(self, n):
        # 6 -> 06
        # 12 -> 12
        if(len(str(n)) == 1):
            return str("0" + str(n))
        return str(n)

    @abstractmethod
    def Crawl(self):
        pass

class Kakao(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            if(len(self.date[n-1].text)<3):# 몇개의 게시물의 날짜가 표시되지 않는다, 게시글까지 타고 들어가서 날짜를 가져온다
                self.setSoup(self.atag[n-1].get('href'))
                
                date_branch = self.soup.select('span.txt_date')
                self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : date_branch[0].text})
                print(url.text +" "+ self.atag[n-1].get('href') +" "+ date_branch[0].text)
            else:
                self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : self.date[n-1].text})
                print(url.text +" "+ self.atag[n-1].get('href') +" "+ self.date[n-1].text)
            n += 1  
        
        return self.arr


class Woowa(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 포멧 맞추기
            dateText = self.date[n-1].text
            dateEnd = dateText.find(",")+1
            subdate = dateText[0:dateEnd+5]
            resdate = str(subdate[subdate.find(",")+2:subdate.find(",")+6]) + "." + str(self.dayFarmat(self.dateMatcher[subdate[0:3]]))  + "." + str(self.dayFarmat(subdate[4:subdate.find(",")]))

            self.arr.append({"title" : url.text, "url" : "http://woowabros.github.io" + self.atag[n-1].get('href'), "date" : resdate})
            print(url.text +" "+ "http://woowabros.github.io" + self.atag[n-1].get('href') +" "+ resdate)
            n += 1  
        return self.arr

        
class Cupang(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 가져오기 (년도가 생략돼있으면 올해 포스트한 글이다)
            print(self.date[n-1].text)
            dateText = self.date[n-1].text
            if(len(dateText) <= 8):
                year = "2019"
            else:
                year = dateText[dateText.find(",")+2 : dateText.find(",")+6]
            
            month = self.dateMatcher[self.dayFarmat(dateText[0:3])]
            day = self.dayFarmat(dateText[4:5])
            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') +" "+ resDate)
            n += 1
        return self.arr

class Spoca(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 가져오기
            dateText = self.date[n-1].text
            year = dateText[0:4]
            month = dateText[6:8]
            day = dateText[10:12]
            resDate = year + "." + month + "." + day

            #a 다듬기 ..   . 이 앞에 붙어있다
            resHref = self.atag[n-1].get('href')[self.atag[n-1].get('href').find("/"):len(self.atag[n-1].get('href'))]
            self.arr.append({"title" : url.text, "url" : "https://spoqa.github.io" + resHref, "date" : resDate})
            print(url.text +" "+ "https://spoqa.github.io" + resHref + " " + resDate)
            n += 1  
        return self.arr

class Yanolja(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 만들기
            dateText = self.date[n-1].text
            year = dateText[7:11]
            month = self.dateMatcher[dateText[3:6]]
            day = dateText[0:2]
            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : "https://yanolja.github.io" + self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ "https://yanolja.github.io" + self.atag[n-1].get('href') + " " + resDate)
            n += 1  
        return self.arr

class Lezhin(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 만들기
            dateText = self.date[n-1].text
            year = dateText[1:5]
            month = dateText[6:8]
            day = dateText[9:11]
            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1  
        return self.arr

class Line(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            dateText = self.date[n-1].text
            resDate = dateText[3:13]

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1  
        return self.arr


class Airbnb(Crawler):
    def Crawl(self):
        path = ["ai", "data", "airbnb-engineering-infrastructure", "web", "fintech", "medium-com-airbnb-engineering-people"]
        for i in path:
            self.setSoup('https://medium.com/airbnb-engineering/'+str(i)+'/home')

            n = 1
            for url in self.urls:
                dateText = self.date[n-1].text
                if(len(dateText) <= 8):
                    year = "2019"
                else:
                    year = dateText[dateText.find(",")+2 : dateText.find(",")+6]
                
                month = self.dateMatcher[self.dayFarmat(dateText[0:3])]
                day = self.dayFarmat(dateText[4:5])
                resDate = year + "." + month + "." + day

                self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
                print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
                n += 1  
        return self.arr

class Google(Crawler):
    def Crawl(self):
        n = 1

        for url in self.urls:
            dateText = self.date[n-1].text
            dateText_sub = dateText[dateText.find(",")+2:len(dateText)]
            year = dateText_sub[dateText_sub.find(",")+2 : dateText_sub.find(",")+6]
            month = self.dateMatcher[dateText_sub[0:3]]
            day = self.dayFarmat(dateText_sub[dateText_sub.find(" ")+1:dateText_sub.find(",")])
            
            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1  

        return self.arr

class Facebook(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            # 날짜 만들기
            dateText = self.date[n-1].text
            year = self.dayFarmat(dateText[dateText.find("년")-4:dateText.find("년")].strip())
            month = self.dayFarmat(dateText[dateText.find("월")-2:dateText.find("월")].strip())
            day = self.dayFarmat(dateText[dateText.find("일")-2:dateText.find("일")].strip())

            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1  
        return self.arr


class Netflix(Crawler):
    def Crawl(self):
        n = 1
        for url in self.urls:
            dateText = self.date[n-1].text
            if(len(dateText) <= 8):
                year = "2019"
            else:
                year = dateText[dateText.find(",")+2 : dateText.find(",")+6]
            
            month = self.dateMatcher[self.dayFarmat(dateText[0:3])]
            day = self.dayFarmat(dateText[4:5])
            resDate = year + "." + month + "." + day
            print(resDate)

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1  

        return self.arr


class Riot(Crawler):
    def Crawl(self):
        n = 1

        for url in self.urls:
            self.setSoup("https://technology.riotgames.com" + self.atag[n-1].get('href'))

            date = self.soup.select('time.c-header__date')
            dateText = date[0].text

            year = dateText[len(dateText)-5:len(dateText)-1]
            month = self.dateMatcher[dateText[1:4]]
            day = self.dayFarmat(dateText[5:dateText.find(',')])

            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : "https://technology.riotgames.com" + self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ "https://technology.riotgames.com" + self.atag[n-1].get('href') + " " + resDate)
            n += 1  

        return self.arr

class GooglePlay(Crawler):
    def Crawl(self):
        n = 1

        for url in self.urls:
            dateText = self.date[n-1].text
            if(len(dateText) <= 8):
                year = "2019"
            else:
                year = dateText[dateText.find(",")+2 : dateText.find(",")+6]
            
            month = self.dateMatcher[self.dayFarmat(dateText[0:3])]
            day = self.dayFarmat(dateText[4:5])
            resDate = year + "." + month + "." + day

            self.arr.append({"title" : url.text, "url" : self.atag[n-1].get('href'), "date" : resDate})
            print(url.text +" "+ self.atag[n-1].get('href') + " " + resDate)
            n += 1
        
        return self.arr


class CrawlerOnChrome:
    def __init__(self, url):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.url = url
        self.arr = []
        self.driver = None

    def Crawl(self):
        self.driver = webdriver.Chrome(executable_path="/root/tech_blog_crawler/chromedriver",chrome_options=self.chrome_options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.url)
        arr = self.findElement()
        self.driver.quit()
        return arr
    
    
    @abstractmethod
    def findElement(self):
        pass

class NHN(CrawlerOnChrome):
    def findElement(self):
        for i in range(1, 13):
            title = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/li['+str(i)+']/a/div/h3').text
            atag = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/li['+str(i)+']/a').get_attribute('href')
            date = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/li['+str(i)+']/a/div/div[2]/span[1]').text
            date = date[4:len(date)]
            self.arr.append({"title" : title, "url" : atag, "date" : date})
            print(title +" "+ atag + " " + date)
        return self.arr

class NaverD2(CrawlerOnChrome):
    def findElement(self):
        for i in range(1, 21):
            title = self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div['+str(i)+']/div/h2/a').text
            atag = self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div['+str(i)+']/div/h2/a').get_attribute('href')
            date = self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div['+str(i)+']/div/dl/dd[1]').text
            self.arr.append({"title" : title, "url" : atag, "date" : date})
            print(title +" "+ atag + " " + date)
        return self.arr

if __name__ == "__main__":
    data = {}

    data["카카오"] = Kakao("https://tech.kakao.com/blog/page/1/#posts",
                            'ul.list_post strong.tit_post',
                            '#posts > div > div.wrap_post > ul > li a.link_post',
                            '#posts > div > div.wrap_post > ul > li > a.link_post > span').Crawl()
    
    data["우아한 형제들"] = Woowa("http://woowabros.github.io/?source=post_page-----e2d736d0e658----------------------",
                                'body > div.page-content > div > section > div > div > a > h2',
                                'body > div.page-content > div > section > div > div > a',
                                'body > div.page-content > div > section > div > div > span').Crawl()

    data["쿠팡"] = Cupang('https://medium.com/coupang-tech/technote/home',
                            'div > div > div > section > div > div > div > a > h3 > div',
                            'div.col.u-xs-marginBottom10.u-paddingLeft0.u-paddingRight0.u-paddingTop15.u-marginBottom30 > a',
                            'div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > time').Crawl()
    
    data["스포카"] = Spoca("https://spoqa.github.io",
                            'body > div > div.content > div.posts > ul > li > div > h2 > a > span',
                            'body > div > div.content > div.posts > ul > li > div > h2 > a',
                            'body > div > div.content > div.posts > ul > li > div > span.post-date').Crawl()

    data["야놀자"] = Yanolja('https://yanolja.github.io/',
                            '#content > article > header > h2 > a',
                            '#content > article > header > h2 > a',
                            '#content > article > footer > time').Crawl()

    data["레진"] = Lezhin('https://tech.lezhin.com/',
                            'body > div.site-wrapper > div > ul.post-list > li > h2 > a',
                            'body > div.site-wrapper > div > ul.post-list > li > h2 > a',
                            'body > div.site-wrapper > div > ul.post-list > li > div.post-meta > p.post-date').Crawl()

    data["라인"] = Line('https://engineering.linecorp.com/ko/blog/page/1/?source=post_page-----e2d736d0e658----------------------',
                        'article > div > header > div > h2 > a',
                        'article > div > header > div > h2 > a',
                        'article span.byline').Crawl()

    data["에어비앤비"] = Airbnb('https://medium.com/airbnb-engineering/',
                                'h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32 div',
                                'a:has(> h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32)',
                                'div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > time').Crawl()

    data["구글"] = Google('https://developers.googleblog.com/?source=post_page-----e2d736d0e658----------------------',
                        'div.post > h2 > a',
                        'div.post > h2 > a',
                        'span.publishdate').Crawl()

    data["페이스북"] = Facebook('https://developers.facebook.com/blog/',
                                'h2._1jlv._7p3_._66wj',
                                'a._8xd-._8xdi._8zgc._8zgd',
                                'div._6z8e > div._6z8b > div._6z8a').Crawl()
    
    data["넷플릭스"] = Netflix('https://medium.com/netflix-techblog',
                            'h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32 > div',
                            'a:has(> h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32)',
                            'div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > time').Crawl()

    data["라이엇게임즈"] = Riot('https://technology.riotgames.com/?source=post_page-----e2d736d0e658----------------------',
                                'h1.c-excerpt__title > a',
                                'h1.c-excerpt__title > a',
                                "lazy setting").Crawl()

    data["구글플레이"] = GooglePlay('https://medium.com/googleplaydev/tagged/android-app-development',
                                    'h3.graf.graf--h3.graf-after--figure.graf--title',
                                    'a:has( h3.graf.graf--h3.graf-after--figure.graf--title)',
                                    'div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > a > time').Crawl()

    data["NHN"] = NHN('https://meetup.toast.com/').Crawl()
    data["NAVER D2"] = NaverD2('https://d2.naver.com/home?source=post_page-----e2d736d0e658----------------------').Crawl()

    # 모든 내용 json 파일화
    file = open('result.json','w', -1, "utf-8")
    json.dump(data, file, ensure_ascii=False)
    file.close()