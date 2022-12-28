########################
#
# Script to generate random user-like traffic
# Jon Estlander / December 2022
#
# Algorithm:
#   Gets a list of top sites from a local file
#   Pick one of those sites in random and get the front page
#   Repeat N times:
#     List all links on that page
#     Pick one link in random and get that page
#
# Installation:
# Works at least with Python 3.7
# Install on Mac:
#   sudo easy_install pip
#   sudo pip install requests
#   sudo pip install beautifulsoup4
#
# Intall on CentOS (you need the EPEL repo for this):
#   sudo yum install python-pip
#   sudo pip install requests
#   sudo pip install beautifulsoup4
# 
# Should run on any linux distribution
# Also runs on Windows 10
#
# Tweakable variables: 
#  ietrations 	int		number of iterations done on the URL list
#  max	 	int		number of iterations done for one site, how deep to go
#  proxies	array		explicit proxies to use, empty array if direct connection
#  follow_relative  True/False	Following these will make the crawler spend more time on the same site
#  urls_file	False/filename  Whether to use alexa or a local file for sites. False = use alexa.com

iterations = 50
max = 30
follow_relative = False
urls_file = "urls.txt"

from bs4 import BeautifulSoup
import requests
import random
import urllib3
urllib3.disable_warnings()
from datetime import datetime
import os,signal

print ("\n---- START: ",datetime.now().strftime("%Y-%m-%d %H:%M:%S")," ----\n")

# See if ahven already is running, and kill it if it is. Useful is ahven is ran by cron or similar, and might be stuck.
#for line in os.popen("ps ax | grep ahven | egrep -v 'grep|vi'"):
#  print(line)
for line in os.popen("ps ax | grep ahven | egrep -v 'grep|vi' | wc -l"):
  if int(line) > 1:
    for process in os.popen("ps ax | grep ahven | egrep -v 'grep|vi' | head -1"):
      fields = process.split()
      pid = fields[0]
      os.kill(int(pid), signal.SIGKILL)
      print("Killed old ahven process: ", pid, "\n")

# Comment out one of these:
#proxies = { "http": "http://192.168.1.21:8080", "https": "http://192.168.1.21:8080" }
proxies = []

badsites = [ "https://secure.eicar.org/eicar.com", "http://users.abo.fi/jestland/eicar.com", "http://adultfriendfinder.com/go/page/reg_form_video_02?pid=g242405-pct.subastfromframe", "http://www.insecure.org", "http://content.pop6.com/images/ffadult/30151/scene_1.flv" ]
badsitefrequency = 20	# Every random n site will be a bad site

# Sites to skip if reached, always do avoid social media:
skipsites = { "facebook.com", "twitter.com" }

user_agent = {'User-agent': 'Ahven/Python Web Crawler'}


# First, lets generate a list of sites to iterate

sites = []

if urls_file: 		# Read the sites from a local file
  f = open(urls_file, "r")
  for x in f:
    sites.append(x.rstrip('\n'))
  f.close()
  print("Got " + str(len(sites)) + " sites from urls_file " + urls_file)

else:
  print ("No URL file found, quitting.")
  exit(1)
 
# Now lets take one site at a time, get the links on that site, and choose one of the links at random

i = 0
while (i < iterations):
  i += 1
  print ("")

  random.seed()
  if (random.randint(1,badsitefrequency) == 1):
    link = badsites[random.randint(0,len(badsites)-1)] 
    print ("Using bad site: " + link)
    url = link
  else:
    link = random.choice(sites)
    print ("Starting iteration number " + str(i) + " for site: " + link )
    url = "https://" + link
  n = 0
  loopcounter = 0
  while n < max:

    while n < max:            # Get the page and look for errors.
      #print ("URL " + str(n) + ": " + str(url.encode('utf-8').strip()))
      print ("URL " + str(n) + ": " + url)
      try:
        r  = requests.get(url, proxies=proxies, headers=user_agent, verify=False)
      except requests.exceptions.ConnectionError as e:
        print ("Can't get that url (ConnectionError).")
        if n > 0:
          if 'links' in locals():		# links is defined
            if len(links) > 1:		# There are alternatives to go to
              url = random.choice(links)
            else:
              url = "http://" + random.choice(sites)
          else:
            url = "http://" + random.choice(sites)
        else: 		# There is an error on the topsite url
          url = "http://" + random.choice(sites)
        n += 1
      except requests.exceptions.ContentDecodingError as e:
        print ("Can't get that url (ContentDecodingError).")
        url = random.choice(links)
#     except requests.exceptions.TypeError as e:
#       print ("Can't get that url (TypeError).")
#       url = random.choice(links)
      else:
        break
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    links=[]
    for anchor in soup.find_all('a'):
      if not anchor.get('href') is None:
        if anchor.get('href')[:4] == "http": 	# Absolute link
          links.append(anchor.get('href'))    
        if follow_relative:
          if anchor.get('href')[:1] == "/": 	# Relative link
            links.append(url+anchor.get('href'))    

    if len(links) > 0:
      link = random.choice(links)
      for s in skipsites:
        if s in link:
          print ("Skipsite found: " + link)
          n = max
      if url == link:
        loopcounter+=1
        if loopcounter == 3:
          print ("Loop detected")
          n = max
      else:
        loopcounter = 0
      if n < max:
        url = link
        n+=1
    else:
      print ("No links on that page")
      n = max

print("\n---- STOP:  ",datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Max iterations reached, closing ----\n")
