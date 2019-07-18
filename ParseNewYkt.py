import requests
from bs4 import BeautifulSoup
import html2text

while(True):
    try:
        mode=int(input("Выберите мод от 1 до 4! (1 - выбрать новость, 2 - несколько новостей, 3-выбрать новости по дням, 4-поиск по ключ. словам):   "))
        if(mode<=4):
            mode=str(mode)
            break
    except ValueError:
        pass


mainUrl="https://news.ykt.ru"
searchUrl='/article/index?page='
tegHref="n-popular_post_title_link"
tegTime="n-popular_post_meta_cdate"

def KnowTheTime(data,tegTime,array):
    if(data.find(tegTime)!=-1):
        time=""
        lineNumber=data.find(">")+1
        for y in data[lineNumber:]:
            if(y=="<"):
                break
            time+=y
        array+=[time]
    return array

def GetDataFromTheSite(mainUrl,searchUrl,numberPages,tegHref,tegTime):
    url = mainUrl+searchUrl+numberPages
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    arrayOfLinks=[]
    arrayOfTimes=[]
    for i in str(soup).splitlines():
        if(i.find(tegHref)!=-1):
            href=""
            numberLink=i.find("href=")+6
            for y in i[numberLink:]:
                if(y=="\""):
                    break
                href+=y
            arrayOfLinks+=[mainUrl+href]
        KnowTheTime(i,tegTime,arrayOfTimes)
    return arrayOfLinks,arrayOfTimes

def HtmlToTxt(url,articleNumber,time):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    f = open(str(articleNumber)+'text.txt', 'w')
    f.write((time + '\n'))
    for i in str(soup).splitlines():
        if(i.find("<p class=")!=-1 or i.find("<p>")!=-1):
            y=html2text.html2text(i)
            if(y.find("[![](")!=-1):
                cache=y.find(")](")
                y=y[5:cache]
                f.write((mainUrl+y + '\n'))
            else:
                f.write((y + '\n'))
    f.close()

if(mode=="1"):
    print("1 - выбрать новость")
    while(True):
        try:
            articleNumber=int(input("Укажите номер статьи:  "))
            break
        except ValueError:
            pass
    numberPages=str(int(articleNumber/36)+1)
    arrayOfLinks,arrayOfTimes=GetDataFromTheSite(mainUrl,searchUrl,numberPages,tegHref,tegTime)
    moduleArticleNumber=articleNumber%36
    url = arrayOfLinks[moduleArticleNumber]
    print(arrayOfTimes[moduleArticleNumber])
    HtmlToTxt(url,articleNumber,arrayOfTimes[moduleArticleNumber])
'''
if(mode=="2"):
    print("2 - несколько новостей")
    while(True):
        try:
            startingPoint=int(input("Укажите начало:  "))
            endingPoint=int(input("Укажите конец:  "))
            break
        except ValueError:
            pass
    
    numberPages=str(int(articleNumber/36)+1)
    arrayOfLinks,arrayOfTimes=GetDataFromTheSite(mainUrl,searchUrl,numberPages,tegHref,tegTime)
    moduleArticleNumber=articleNumber%36
    url = arrayOfLinks[moduleArticleNumber]
    print(arrayOfTimes[moduleArticleNumber])
    HtmlToTxt(url,articleNumber,arrayOfTimes[moduleArticleNumber])
'''