from bs4 import BeautifulSoup
import requests

URL = "https://wikis.fandom.com/wiki/Category:Games_hub"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

encoded_html = soup.prettify("utf-8")

wikitable = soup.find(class_="mw-parser-output")


data = wikitable.find_all("tr", limit=6)
data = data[5]
data = str(data)

#print(data)

titleIndex = [i for i in range(len(data)) if data.startswith(" title=", i)] 
#print(titleIndex)

wikiIndex = [i for i in range(len(data)) if data.startswith(r'">', i)] 
#print(wikiIndex) Wiki"

print(len(titleIndex))
print(len(wikiIndex))

games = []

for x in titleIndex:
    #print(data[x + 7: wikiIndex[titleIndex.index(x)]])
    name = data[x + 7: wikiIndex[titleIndex.index(x)]]
    name = name.replace('"', "")
    name = name.replace(" Wiki", "")

    games.append(name)


print(games)


"""f = open("test.txt","w+")
f.write(data)
f.close()"""