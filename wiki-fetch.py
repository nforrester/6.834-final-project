#!/usr/bin/env python3

import urllib.parse
import urllib.request
import json
import re

def fetch(title):
  url = 'http://en.wikipedia.org/w/api.php'
  user_agent = '6.834ClassProject/0.1 (nforrest@mit.edu)'
  values = { 'format' : 'json'
           , 'action' : 'query'
           , 'titles' : title
           , 'prop'   : 'revisions'
           , 'rvprop' : 'content'
           }
  headers = { 'User-Agent' : user_agent }

  data = urllib.parse.urlencode(values).encode()
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  the_page = response.read()

  json_data = json.loads(the_page.decode())
  wikitext = list(json_data['query']['pages'].values())[0]['revisions'][0]['*']
  return wikitext

def link_words(wikitext):
  link_regex = re.compile('\[\[[^:#\[\]]+\]\]')
  links = re.findall(link_regex, wikitext)

  title_regex = re.compile('\[[^\[\]\|]*[|\]]')
  words_regex = re.compile('[^ |\\\\\[\]\(\)]+')
  return [re.findall(words_regex, re.findall(title_regex, link)[0]) for link in links]

print(link_words(fetch('Eurasian lynx')))
