import requests
import bs4

KEYWORDS = {"дизайн", "фото", "web", "python", "искусственный интеллект", "ии"}

SEARCHWORDS = {"робот", "програмирование", "машинное обучение", "искусственный интеллект", "ии"}

HEADERS = {"Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "ru-RU,ru;q=0.8",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
}

PAGES = 3

pages = range(PAGES)
for page in pages:
    add_url = f"page{page + 1}"
    response = requests.get("https://habr.com/ru/all/" + add_url, headers=HEADERS)
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all(class_="tm-article-snippet")

    for article in articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = {hub.find("a").text.strip().lower() for hub in hubs}
        if hubs & KEYWORDS:
            article_tag_a = article.find("h2").find("a")
            href = article_tag_a.attrs["href"]
            url = "https://habr.com" + href
            print("--------------------------------------------------------------------------------")
            print(article_tag_a.text, "-->",  url)
            print(f"Теги: {', '.join(hubs & KEYWORDS)}")

            response = requests.get(url, headers=HEADERS)
            text = response.text

            soup = bs4.BeautifulSoup(text, features="html.parser")
            articles = soup.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
            bodys = article.find_all("p")
            body = " ".join('%s' %id for id in bodys)
            for i in SEARCHWORDS:
                j = body.lower().find(i)
                if j != -1:
                    print(f"'{i}' встречается в статье {j} раз")
