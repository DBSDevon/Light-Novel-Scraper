#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
import string

# Initalizing some variables used throughout the code #
url_list = []
ch_num_list = []
temp_url_list = []
temp_num_list = []
skip = False
start_page_obj = None

soup = None

# Grabs novel title from user, and changes it into correct format. #
# Removes capitlization, puncutation, and replaces spaces with '-' #
def user_input():
  novel_title = str(input('What novel would you like to download? \n')).lower()
  novel_title = re.sub(r'[^\w\s]','',novel_title)
  novel_title=(novel_title.translate(str.maketrans('', '', string.punctuation))).replace(' ', '-')

  return novel_title


while start_page_obj is None and skip is False:

  novel_title = user_input()
  link_source = 'https://www.novelupdates.com/series/' + novel_title + '/?pg=999'
  page = requests.get(link_source)
  soup = BeautifulSoup(page.text, 'html.parser')
  start_page_obj = soup.find(class_='digg_pagination')
  if start_page_obj is None:
    start_page_table = soup.find(id='myTable')
    if start_page_table is not None:
      skip = True

  if start_page_obj is None and skip is False:
    print("No novel found. Please re-enter the name of the novel.")

curr_page_num = 1

# Find's the last page listed, then reassigns start page.  #
# Skips this step if there is only one page.               #

if(start_page_obj):
  start_page_list = start_page_obj.find_all("em")
  for item in start_page_list:
    curr_page_num = item.contents[0]

# Helper method to grab all chapter numbers and links on current page #
def get_ch_nums_and_links(url):
    currpage = requests.get(url)
    currsoup = BeautifulSoup(currpage.text, 'html.parser')
    start_page_obj = currsoup.find(id='myTable')
    start_page_list = start_page_obj.find_all('a', {'class':"chp-release"})

    global url_list
    global ch_num_list
    temp_url_list = []
    temp_num_list = []

    # Grabs every chapter link and chapter number on the current page #
    # Removes first two characters of url as novel updates saves      #
    # their links with // in the beginning                            #
    for item in start_page_list:
        url = item.get('href')
        url = url[2:]
        ch_nums = item.contents[0]
        temp_num_list.append(ch_nums)
        temp_url_list.append(url)

    # Adds the new chapter links and numbers to complete list. #
    temp_num_list.reverse()
    temp_url_list.reverse()
    ch_num_list = ch_num_list + temp_num_list
    url_list = url_list + temp_url_list


# Runs through every page until the newest chapter has been reached #
while curr_page_num != 0:
    curr_page_html = 'https://www.novelupdates.com/series/' + novel_title + '/?pg=' + str(curr_page_num)
    curr_page_num = int(curr_page_num) - 1
    get_ch_nums_and_links(curr_page_html)

#print (url_list)
#print (ch_num_list)

print ("Select Download type")
file_type = ""


while file_type != "A" and file_type != "B" and file_type != "C":
    file_type = str(input('Would you like to download this light novel as \n'
    '(A) - .html files \n'
    '(B) - .pdf files \n'
    '(C) - as an ePub? \n'))

    if file_type != "A" and file_type != "B" and file_type != "C":
        print ("Invalid Input!")
        print ("Please choose A, B, or C")
