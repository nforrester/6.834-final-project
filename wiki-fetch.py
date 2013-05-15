#!/usr/bin/env python3

import urllib.parse
import urllib.request
import json
import re
import sys

def api_call(values):
  url = 'http://en.wikipedia.org/w/api.php'
  user_agent = '6.834ClassProject/0.1 (nforrest@mit.edu)'
  headers = { 'User-Agent' : user_agent }

  data = urllib.parse.urlencode(values).encode()
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  the_page = response.read()

  json_data = json.loads(the_page.decode())
  return json_data

def page_content(title):
  return api_call({ 'format' : 'json'
                  , 'action' : 'query'
                  , 'titles' : title
                  , 'prop'   : 'revisions'
                  , 'rvprop' : 'content'
                  })


def wikitext(json_data):
  return list(json_data['query']['pages'].values())[0]['revisions'][0]['*']

def kill_nowiki(wikitext):
  nowiki_re = re.compile('<nowiki>.*?</nowiki>')
  return ''.join(re.split(nowiki_re, wikitext))

def expandtemplates(query_result):
  page = list(query_result['query']['pages'].values())[0]
  revision = page['revisions'][0]
  return api_call({ 'format'      : 'json'
                  , 'action'      : 'expandtemplates'
                  , 'title'       : page['title']
                  , 'text'        : revision['*']
                  , 'generatexml' : False
                  })

def link_words(wikitext):
  link_regex = re.compile('\[\[[^:#\[\]]+\]\]')
  links = re.findall(link_regex, wikitext)

  title_regex = re.compile('\[[^\[\]\|]*[|\]]')
  words_regex = re.compile('[^ |\\\\\[\]\(\)]+')
  return [re.findall(words_regex, re.findall(title_regex, link.lower())[0]) for link in links]

def categories(title):
  json_data = api_call({ 'format' : 'json'
                       , 'action' : 'query'
                       , 'titles' : title
                       , 'prop'   : 'categories'
                       , 'clshow' : '!hidden'
                       })
  try:
    return [x['title'] for x in list(json_data['query']['pages'].values())[0]['categories']]
  except KeyError as e:
    return []

category_graph = {}

def category_graph_add(category):
  if not(category in category_graph):
    print('Adding category: ' + category)
    cats = categories(category)
    category_graph[category] = cats
    print(category + ' is in:')
    for cat in cats:
      print('   ' + cat)

def category_graph_fetch(category):
  if not(category in category_graph):
    category_graph_add(category)
  return category_graph[category]

def categories_to_depth(category, depth):
  cats = category_graph_fetch(category)
  final_set = set(cats)
  if depth > 0:
    for cat in cats:
      final_set = final_set | categories_to_depth(cat, depth - 1)
  return final_set

cats = categories_to_depth('Albert Einstein', 6)
print('')
print('Final list of categories(6):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 5)
print('')
print('Final list of categories(5):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 4)
print('')
print('Final list of categories(4):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 3)
print('')
print('Final list of categories(3):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 2)
print('')
print('Final list of categories(2):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 1)
print('')
print('Final list of categories(1):')
for cat in cats:
  print(cat)
cats = categories_to_depth('Albert Einstein', 0)
print('')
print('Final list of categories(0):')
for cat in cats:
  print(cat)

#print(link_words(wikitext(page_content('Eurasian lynx'))))

#t = 'Category:1970s births'
#print(expandtemplates(page_content(t))['expandtemplates']['*'])
#print(categories(t))
