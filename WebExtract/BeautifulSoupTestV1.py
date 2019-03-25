"""
Trialling BeautifulSoup package as seems to be best for webscraping in python/
Website: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

23/03/19: initial commit
Author: Calum Towler
"""

example_html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(example_html_doc, 'html.parser')

print(soup.prettify())