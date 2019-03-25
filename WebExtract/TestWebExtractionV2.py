"""
Second attempt at extracting information from google finance using python.
Method comes from https://www.youtube.com/watch?v=A61EF6TTCow

Created on Sat Mar 23 10:21:54 2019

Author: Calum Towler
"""

import urllib
#html = urllib.request.urlopen('https://www.google.co.uk/finance')
#html = html.readlines()


req = Request('https://www.google.co.uk/finance', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

print(webpage)
