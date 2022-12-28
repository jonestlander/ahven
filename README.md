# ahven
# Script to generate random user-like traffic
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
