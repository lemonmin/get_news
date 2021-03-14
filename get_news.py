from bs4 import BeautifulSoup
import requests
from datetime import datetime



today = datetime.today().strftime("%Y%m%d_%H:%M:%S") # 오늘 날짜시간을 YYYYMMDD_HH:MM:SS 형태로 출력
category_list = [("OTT","https://news.google.com/search?q=OTT&hl=en-US&gl=US&ceid=US%3Aen"), # Google news에서 OTT로 검색한 URL, 한국지역 말고 미국으로 검색함
                ("Disney+","https://news.google.com/search?q=Disney%2B&hl=en-US&gl=US&ceid=US%3Aen"), # Disney+
                ("SlingTV","https://news.google.com/search?q=SlingTV&hl=en-US&gl=US&ceid=US%3Aen"), # SlingTV
                ("Xfinity Stream","https://news.google.com/search?q=Xfinity%20Stream&hl=en-US&gl=US&ceid=US%3Aen"),
                ("Peacock","https://news.google.com/search?q=Peacock&hl=en-US&gl=US&ceid=US%3Aen")]
news_container = []

def get_news_list(url):
    news_lists_container = []
    res = requests.get(url)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        src = res.text
        # BeautifulSoup(html 소스코드, 이용할 parser 명시)
        # html 소스를 python 객체로 변환하기
        soup = BeautifulSoup(src, 'html.parser')
        # css 선택자를 이용해 하나의 html 요소를 찾는 함수
        # 참고로 구글 개발자도구에서 특정 요소 우클릭 > Copy > Copy selector로 해당 요소의 css선택자를 복사해올 수 있음
        #search_box = soup.select_one("#gb > div.gb_Kd.gb_4d.gb_Td > div.gb_Jd.gb_Wd.gb_Ie.gb_Le > div > form > div.gb_vf > div > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd")
        news_list = soup.find("div", {"class": "lBwEZb BL5WZb xP6mwf"})
        for item in news_list:
            link_tag = item.find("a", {"class":"VDXfz"})
            if link_tag != None:
                link = link_tag['href']
            else:
                link = "None"
            date_tag = item.find("time", {"class":"WW6dff uQIVzc Sksgp"})
            if date_tag != None:
                date = date_tag['datetime']
            else:
                date = "None"
            title_tag = item.find("a", {"class":"DY5T1d RZIKme"})
            if title_tag != None:
                title = title_tag.get_text()
            else:
                title = "None"
            # print("*title : ", title, "\n* link : ",link,"\n* date : ",date)
            # print("**"*20)
            temp = {"title":title, "link":link, "date":date}
            news_lists_container.append(temp)
    else :
        print(res.status_code)
    return news_lists_container

def make_page():
    h = "<html>"
    h += """
    <head>
    <style>
    table, th, td {
      border-right:none;
      border-left:none;
      border-top: 1px solid #d1d6db;
      border-bottom:1px solid #d1d6db;
      border-collapse: collapse;
    }
    </style>
    </head>
    """
    h += "<body>"
    for item in news_container:
        h += "<details><summary>"+item[0]+"</summary><div><table>"
        for i in item[1]:
            h += "<tr><td><a href='https://news.google.com/"+i["link"]+"'>"+i["title"]+"</a></td></tr>"
        h += "</table></div></details>"
    h+= "</body></html>"
    file = open("news_"+str(today).split("_")[0]+".html", "w+", encoding="utf-8")
    file.write(h)
    file.close()

for url in category_list:
    news_container.append((url[0], get_news_list(url[1])))
    # print("==="*50)

make_page()
