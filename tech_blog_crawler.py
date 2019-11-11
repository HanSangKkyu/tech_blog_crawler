import requests
from bs4 import BeautifulSoup
import json
import os

from urllib.request import urlopen
import ssl

data = {}

# 카카오
for i in range(1, 14):
    context = ssl._create_unverified_context()
    res = urlopen("https://tech.kakao.com/blog/page/"+str(i)+"/#posts", context=context)
    soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')

    urls = soup.select('ul.list_post strong.tit_post')
    atag = soup.select('#posts > div > div.wrap_post > ul > li a.link_post')


    n = 1
    arr = []
    for url in urls:
        arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
        print(url.text +" "+ atag[n-1].get('href'))
        n += 1  
    
    data["카카오"] = arr
    

# # 우아한 형제들
# context = ssl._create_unverified_context()
# res = urlopen("http://woowabros.github.io/?source=post_page-----e2d736d0e658----------------------", context=context)
# soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')

# urls = soup.select('body > div.page-content > div > section > div > div > a > h2')
# atag = soup.select('body > div.page-content > div > section > div > div > a')


# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : "http://woowabros.github.io" + atag[n-1].get('href')})
#     print(url.text +" "+ "http://woowabros.github.io" + atag[n-1].get('href'))
#     n += 1  

# data["우아한 형제들"] = arr


# # 쿠팡
# res = requests.get('https://medium.com/coupang-tech/technote/home')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('div > div > div > section > div > div > div > a > h3 > div')
# atag = soup.select('div.col.u-xs-marginBottom10.u-paddingLeft0.u-paddingRight0.u-paddingTop15.u-marginBottom30 > a')

# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1  

# data["쿠팡"] = arr



# # 스포카
# for i in range(1, 12):
#     if(i == 1):
#         context = ssl._create_unverified_context()
#         res = urlopen("https://spoqa.github.io", context=context)
#         soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')
#     else:
#         context = ssl._create_unverified_context()
#         res = urlopen("https://spoqa.github.io/page"+str(i), context=context)
#         soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')

#     urls = soup.select('body > div > div.content > div.posts > ul > li > div > h2 > a > span')
#     atag = soup.select('body > div > div.content > div.posts > ul > li > div > h2 > a')


#     n = 1

#     arr = []
#     for url in urls:
#         arr.append({"title" : url.text, "url" : "https://spoqa.github.io" + atag[n-1].get('href')})
#         print(url.text +" "+ "https://spoqa.github.io" + atag[n-1].get('href'))
#         n += 1  
    
#     data["스포카"] = arr 

# # 야놀자
# for i in range(1, 3):
#     if(i == 1):
#         res = requests.get('https://yanolja.github.io/')
#         html = res.content
#         soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
#     else:
#         res = requests.get("https://yanolja.github.io/page"+str(i))
#         html = res.content
#         soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

#     urls = soup.select('#content > article > header > h2 > a')
#     atag = soup.select('#content > article > header > h2 > a')


#     n = 1

#     arr = []
#     for url in urls:
#         arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#         print(url.text +" "+ atag[n-1].get('href'))
#         n += 1  
    
#     data["야놀자"] = arr

# # 레진
# for i in range(1, 5):
#     if(i == 1):
#         res = requests.get('https://tech.lezhin.com/')
#         html = res.content
#         soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
#     else:
#         res = requests.get("https://tech.lezhin.com/pages/"+str(i))
#         html = res.content
#         soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

#     urls = soup.select('body > div.site-wrapper > div > ul.post-list > li > h2 > a')
#     atag = soup.select('body > div.site-wrapper > div > ul.post-list > li > h2 > a')


#     n = 1

#     arr = []
#     for url in urls:
#         arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#         print(url.text +" "+ atag[n-1].get('href'))
#         n += 1  
    
#     data["레진"] = arr


# # 피플펀드
# for i in range(1, 19):
#     res = requests.get('https://engineering.linecorp.com/ko/blog/page/'+str(i)+'/?source=post_page-----e2d736d0e658----------------------')
#     html = res.content
#     soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

#     urls = soup.select('article > div > header > div > h2 > a')
#     atag = soup.select('article > div > header > div > h2 > a')

#     n = 1

#     arr = []
#     for url in urls:
#         arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#         print(url.text +" "+ atag[n-1].get('href'))
#         n += 1  
    
#     data["피플펀드"] = arr



# # 에어비엔비
# path = ["ai", "data", "airbnb-engineering-infrastructure", "web", "fintech", "medium-com-airbnb-engineering-people"]
# for i in path:
#     res = requests.get('https://medium.com/airbnb-engineering/'+str(i)+'/home')
#     html = res.content
#     soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

#     urls = soup.select('h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32 div')
#     atag = soup.select('a:has(> h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32)')

#     n = 1

#     arr = []
#     for url in urls:
#         arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#         print(url.text +" "+ atag[n-1].get('href'))
#         n += 1  
    
#     data["에어비엔비"] = arr 



# # 구글 (첫페이지만 가져온다)
# res = requests.get('https://developers.googleblog.com/?source=post_page-----e2d736d0e658----------------------')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('div.post > h2 > a')
# atag = soup.select('div.post > h2 > a')

# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1  

# data["구글"] = arr 



# # 페이스북 (최신 9개만 가져온다)
# res = requests.get('https://developers.facebook.com/blog/')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('h2._1jlv._7p3_._66wj')
# atag = soup.select('a._3els')

# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1  

# data["페이스북"] = arr


# # 넷플릭스 (최신)
# res = requests.get('https://medium.com/netflix-techblog')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32 > div')
# atag = soup.select('a:has(> h3.u-contentSansBold.u-lineHeightTightest.u-xs-fontSize24.u-paddingBottom2.u-paddingTop5.u-fontSize32)')

# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1  

# data["넷플릭스"] = arr


# # 라이엇게임즈 (최신)
# res = requests.get('https://technology.riotgames.com/?source=post_page-----e2d736d0e658----------------------')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('h1.c-excerpt__title > a')
# atag = soup.select('h1.c-excerpt__title > a')

# n = 1

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : "https://technology.riotgames.com" + atag[n-1].get('href')})
#     print(url.text +" "+ "https://technology.riotgames.com" + atag[n-1].get('href'))
#     n += 1  

# data["라이엇게임즈"] = arr



# # 구글플레이 (최신)
# res = requests.get('https://medium.com/googleplaydev/tagged/android-app-development')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('h3.graf.graf--h3.graf-after--figure.graf--title')
# atag = soup.select('a:has( h3.graf.graf--h3.graf-after--figure.graf--title)')

# n = 1

# print(len(urls))
# print(len(atag))

# arr = []
# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1

# res = requests.get('https://medium.com/googleplaydev/tagged/game-development')
# html = res.content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# urls = soup.select('h3.graf.graf--h3.graf-after--figure.graf--title')
# atag = soup.select('a:has( h3.graf.graf--h3.graf-after--figure.graf--title)')

# n = 1

# print(len(urls))
# print(len(atag))


# for url in urls:
#     arr.append({"title" : url.text, "url" : atag[n-1].get('href')})
#     print(url.text +" "+ atag[n-1].get('href'))
#     n += 1  

# data["구글플레이"] = arr




# file = open('result.json','a', -1, "utf-8")
# json.dump(data, file, ensure_ascii=False)
# file.close