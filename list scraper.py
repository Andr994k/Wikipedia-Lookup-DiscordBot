from bs4 import BeautifulSoup
import requests

URL = "https://wikis.fandom.com/wiki/Category:Games_hub"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

encoded_html = soup.prettify("utf-8")

wikitable = soup.find(class_="mw-parser-output")

data = wikitable.find_all("tr", limit=6)

data = data[5]

print(data)



#wikitable = wikitable.prettify("utf-8")

"""f = open("RAWgames.txt","w+")
f.write(str(wikitable))
f.close()"""