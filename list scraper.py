from bs4 import BeautifulSoup
import requests

def Get_List(URL: str):
    LIST = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    wikitable = soup.find(class_="mw-parser-output")

    data = wikitable.find_all("tr", limit=6)
    data = data[5]
    data = str(data)

    titleIndex = [i for i in range(len(data)) if data.startswith(" title=", i)] 
    wikiIndex = [i for i in range(len(data)) if data.startswith(r'">', i)] 

    for x in titleIndex:
        name = data[x + 7: wikiIndex[titleIndex.index(x)]]
        name = name.replace('"', "")
        name = name.replace(" Wiki", "")

        LIST.append(name)

    return LIST

games = Get_List("https://wikis.fandom.com/wiki/Category:Games_hub")
shows = Get_List("https://wikis.fandom.com/wiki/Category:TV_hub")

print(games)
print(shows)