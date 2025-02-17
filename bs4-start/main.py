from bs4 import BeautifulSoup
import requests

# with open("website.html") as file:
#     contents=file.read()
#
# soup=BeautifulSoup(contents,"html.parser")
# print(soup.title)
# print(soup.prettify())

response=requests.get(url="https://news.ycombinator.com/news")
yc_webpage=response.text

soup=BeautifulSoup(yc_webpage,"html.parser")
# print(soup.prettify())
articles=[]
rows = soup.find_all("tr", class_="athing")
for row in rows:
    article_link_tag = row.select_one("span.titleline > a")
    article_name = article_link_tag.text
    article_link = article_link_tag.get("href")

    next_row = row.find_next_sibling("tr")
    score_tag = next_row.select_one("span.score")

    score = score_tag.text.split()[0] if score_tag else None

    articles.append({
        "name": article_name,
        "link": article_link,
        "score": score
    })

sorted_articles = sorted(articles, key=lambda x: int(x["score"]) if x["score"] is not None else 0, reverse=True)

print(sorted_articles[0])