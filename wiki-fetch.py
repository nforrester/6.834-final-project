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
  try:
    page = list(query_result['query']['pages'].values())[0]
    revision = page['revisions'][0]
    return api_call({ 'format'      : 'json'
                    , 'action'      : 'expandtemplates'
                    , 'title'       : page['title']
                    , 'text'        : revision['*']
                    , 'generatexml' : False
                    })
  except KeyError:
    print('key error')
    print(query_result)
    sys.exit(1)

def get_links(title):
  text = kill_nowiki(expandtemplates(page_content(title))['expandtemplates']['*'])
  
  link_regex = re.compile('\[\[[^:#\[\]]+\]\]')
  links = re.findall(link_regex, text)

  title_regex = re.compile('[^\[\]\|]+')
  return set([re.findall(title_regex, link)[0] for link in links])

def link_words(wikitext):
  link_regex = re.compile('\[\[[^:#\[\]]+\]\]')
  links = re.findall(link_regex, wikitext)

  title_regex = re.compile('\[[^\[\]\|]*[|\]]')
  words_regex = re.compile('[^ |\\\\\[\]\(\)]+')
  return [re.findall(words_regex, re.findall(title_regex, link.lower())[0]) for link in links]

def add_dicts(a, b):
  return dict(list(a.items()) + list(b.items()))

def categories(title):
  cats = []
  cont = {}
  while True:
    json_data = api_call(add_dicts({ 'format' : 'json'
                                   , 'action' : 'query'
                                   , 'titles' : title
                                   , 'prop'   : 'categories'
                                   , 'clshow' : '!hidden'
                                   }, cont))

    try:
      cats = cats + [x['title'] for x in list(json_data['query']['pages'].values())[0]['categories']]
    except KeyError as e:
      pass

    try:
      cont = json_data['query-continue']['categories']
    except KeyError:
      break
  return cats

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
  category_graph_add(category)
  return category_graph[category]

def categories_to_depth(category, depth):
  cats = category_graph_fetch(category)
  final_set = set(cats)
  if depth > 0:
    for cat in cats:
      final_set = final_set | categories_to_depth(cat, depth - 1)
  return final_set

def estimate_categories(page):
  # This should actually use the cooccurrance thing
  return category_graph_fetch(page)

def navigate(start, end):
  expansion_depth = 4
  category_preferences = {}
  for i in range(expansion_depth + 1):
    for category in categories_to_depth(end, i):
      if not(category in category_preferences):
        category_preferences[category] = i
  for i in range(expansion_depth + 1):
    for category in categories_to_depth(start, i):
      if not(category in category_preferences):
        category_preferences[category] = expansion_depth * 2 + 2 - i

  def preference(page):
    if page == end:
      return -1
    pref = expansion_depth * 2 + 3
    for category in estimate_categories(page):
      try:
        pref = min(pref, category_preferences[category])
      except KeyError:
        pass
    return pref

  visited = {start: None}
  to_visit = list(map(lambda page: (page, start, preference(page)), get_links(start)))
  while len(to_visit) > 0:
    to_visit.sort(key = lambda x: x[2])
    current = to_visit.pop(0)
    if not(current[0] in visited):
      print('Visiting ' + current[0])
      visited[current[0]] = current[1]
      if current[0] == end:
        print('SUCCESS!')
        this_page = current[0]
        path = []
        while this_page != None:
          path.append(this_page)
          this_page = visited[this_page]
        return path
      to_visit = to_visit + list(map(lambda page: (page, current[0], preference(page)), get_links(current[0])))

print(navigate('Solar storm of 1859', 'Albert Einstein'))

#print(kill_nowiki(expandtemplates(page_content('Balfour Stewart'))['expandtemplates']['*']))

#for link in get_links('Solar storm of 1859'):
#  print(link)

#cats = categories_to_depth('Solar storm of 1859', 6)
#cats = categories_to_depth('Category:Knowledge', 0)
#print('')
#print('Final list of categories:')
#for cat in cats:
#  print(cat)

#print(link_words(wikitext(page_content('Eurasian lynx'))))

#t = 'Category:1970s births'
#print(expandtemplates(page_content(t))['expandtemplates']['*'])
#print(categories(t))
