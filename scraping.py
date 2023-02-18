import requests
from bs4 import BeautifulSoup
from summarize import summarize

def get_from_tirto():
  url = 'https://tirto.id/q/current-issue-hPZ'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  div = soup.find('div', {'class': 'row my-5'})
  articles = div.find_all('div', {'class': 'news-list-fade'})
  article_tirto = []
  for article in articles:
    article_tirto.append({
        "jenis": "tirto",
        "judul": article.find("h1").text,
        "link": "https://tirto.id/"+article.find("a").get("href"),
        "image": article.find("img").get("src"),
    })
  return article_tirto


def get_tirto_article(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  title = soup.find("h1", {"class": "news-detail-title"}).text
  article = soup.find("article")
  article = article.find_all("div", {"class": "content-text-editor"})[0]
  script_tags = article.find_all('script')
  for script_tag in script_tags:
      script_tag.extract()
  script_tags = article.find_all('div', {'class': 'baca-holder'})
  for script_tag in script_tags:
      script_tag.extract()
  article_text = article.get_text(strip=True)
  summarize_text = summarize(article_text, 5)
  return title, summarize_text, article_text

def get_all(page):
    data = []
    data.extend(get_from_tirto())
    return data

def get_article_sum(url, tipe):
    if(tipe == "tirto"):
        title, summarize, article = get_tirto_article(url)
        return ({
            "message": "success",
            "code": 200,
            "data": {
                "title": title,
                "article": summarize,
                "plain_text": article,
                "type": "tirto"
            }
        })
    else:
        return ({
            "message": "error",
            "code": 404,
            "data": {}
        })