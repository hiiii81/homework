import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client=MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# 1~50위의 곡 스크래핑: 순위/곡 제목, 가수 스크래핑해서 출력하기
for tr in trs:
  rank = tr.select_one('td.number').text[0:2].strip()
  title = tr.select_one('td.info > a.title.ellipsis').text.strip()
  artist = tr.select_one('td.info > a.artist.ellipsis').text

  doc = {
     'rank': rank,
     'title': title,
     'artist': artist
  }
  db.musicrank.insert_one(doc)