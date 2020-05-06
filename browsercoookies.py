import browser_cookie3
import re
import json
import requests
from bs4 import BeautifulSoup

cj = browser_cookie3.load()
tescoCookies = []
for c in cj:
    if(re.search('\.tesco\.com', c.domain)):
        tescoCookies.append(c)

s = requests.Session()
for c in tescoCookies:
    # print(c)
    s.cookies.set_cookie(c)


cookies = ''
for c in tescoCookies:
    cookies += c.name + "=" + c.value + "; "


## get csrf
r = requests.get('https://www.tesco.com/groceries/en-GB/trolley', headers={'cookie': cookies})
soup = BeautifulSoup(r.content, 'html.parser')
csrf = soup.find('input', attrs={'name': '_csrf'})['value']

#Add cookies from trolley page to the next requests,
#trolley cookies are needed for the put requests
for i in r.cookies:
	add = True
	for y in tescoCookies:
		if y.name == i.name:
			y.value = i.value
			add = False
			break
	if add:
		tescoCookies.append(i)


cookies = ''
for c in tescoCookies:
    cookies += c.name + "=" + c.value + "; "


## can add with this
data = '{"items":[{"id":"292278149","newValue":0,"oldValue":1,"newUnitChoice":"pcs","oldUnitChoice":"pcs"}]}'
data = '{"items":[]}'
# data = json.dumps(data)
r = requests.put("https://www.tesco.com/groceries/en-GB/trolley/items?_method=PUT", headers={'cookie': cookies,
    'x-csrf-token': csrf,
    'content-type': 'application/json',
    'accept': 'application/json'}
    , data=data)
r = json.loads(r.content)

for item in r['items']:
    print(item['quantity'], item['product']['title'], '£'+str(item['cost']))
