"""
First attempt at extracting information from Google Finance in Python - Google allows this search!
Method comes from https://www.youtube.com/watch?v=4UcqECQe5Kc

23/03/19: initial commit
Author: Calum Towler
"""

import requests
from bs4 import BeautifulSoup
#from csv import writer

response = requests.get('nttps://www.google.co.uk/search?site=finance&tbm=fin&q=INDEXFTSE:+UKX&stick=H4sIAAAAAAAAAONgecRowi3w8sc9YSntSWtOXmNU5eIKzsgvd80rySypFBLnYoOyeKW4uTj1c_UNjDJyzMp5FrHyefq5uEa4hQS7WimEekcAAMw2dBpKAAAA&sa=X&ved=0ahUKEwj5gLf_upjhAhVxunEKHWoeB6QQ0uIBCJYBMBA&biw=1536&bih=754&dpr=1.25#scso=_7ECWXIbEKJm11fAPxdW-uA82:0')
soup = BeautifulSoup(response.text, 'html.parser')
<div class="mw">
print(soup.prettify())

#for link in soup.find_all('a'):
#   print(link.get('href'))

print(soup.get_text())
#posts = soup.find_all(class_='post-preview')

#with open('posts.csv', 'w') as csv_file:
#    csv_writer = writer(csv_file)
#    headers = ['Title', 'Link', 'Date']
#    csv_writer.writerow(headers)

#    for post in posts:
#        title = post.find(class_='post-title').get_text().replace('\n', '')
#        link = post.find('a')['href']
#        date = post.select('.post-date')[0].get_text()
#        csv_writer.writerow([title, link, date])
#
#print(headers)
