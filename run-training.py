import pymysql
import config
import math
import pickle

conn = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db_name, cursorclass=cursor.SSCursor)

# go through each category, get all the pages in that category, count the words in that title
categories = {}

def words_from_title(title):
  # NEIL USE REGEX MAGIC HERE
  return title.split("_")

# select all page names
cur = conn.cursor(pymysql.cursors.SSCursor)
cur.execute("select p.page_title, cl.cl_to from categorylinks cl left join page p on cl.cl_from=p.page_id")

# count up all the data
word_count_key = 'TOTAL_CATEGORY_WORD_COUNT'
article_count_key = 'TOTAL_CATEGORY_ARTICLE_COUNT'
total_number_of_articles = 0
for row in cur.fetchall_unbuffered():
  # initialize the category if we haven't seen it before
  if not categories.has_key(row[1]):
    categories[row[1]] = {
      word_count_key: 0,
      article_count_key: 0
    }

  # add to the article count
  total_number_of_articles += 1
  categories[article_count_key] += 1

  # add to the word count
  for word in words_from_title(row[0]):
    # add the word to the individual category count
    if not categories[row[1]].has_key(word):
      categories[row[1]][word] = 1
    else:
      categories[row[1]][word] += 1
        
    # add to the total count for each category
    categories[row[1]][word_count_key] += 1

# clean up connection
cur.close()
conn.close()

# calculate prior for and correspondences for article-category model
article_category_prior = {}
article_category_correspondences = {}
prior_denominator = math.log(total_number_of_articles)
for cat in categories.keys():
  article_category_prior[cat] = math.log(categories[cat][article_count_key]) - prior_denominator

  correspondences_denominator = math.log(categoires[cat][word_count_key])
  article_correspondences[cat] = {}
  for word in categories[cat].keys():
    article_correspondences[cat][word] = math.log(categories[cat][word]) - correspondences_denominator
  
# save training data
data_file_name = 'article-category-model.data'
with open(data_file_name, 'r') as f:
  pickle.dump(a, {
    'article_category_prior': article_category_prior,
    'article_category_correspondences': article_category_correspondences
  })