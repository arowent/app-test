import requests
from bs4 import BeautifulSoup

with open('/home/arowent/Code/app-test/parse/all.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_username = soup.find_all('div', {'class': 'sc-bdvvtL sc-gsDKAQ sc-hRMWxn sc-fTxOGA ieSfBq klCafx hqRFhs'})

for i in all_username:
    link = i.find('a')
    if 'token' in link.get('href'):
        print(link.get('href'))