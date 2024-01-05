# search_title()

from bs4 import BeautifulSoup
from libgen_api import LibgenSearch
import requests
import urllib.request

def inp_to_int(inp):
	try:
		i = int(inp)
	except:
		i = 0
	return i

s = LibgenSearch()

search_choice = inp_to_int(input("Enter 1 for search by author,any number for search by title."))

if search_choice == 1:
	author = input("Who is the author?")
	results = s.search_author(author)
else:
	title = input("What is the book titled?")
	results = s.search_title(title)


for result in results:
	author = result["Author"]
	title = result["Title"]
	size = result["Size"]
	extention = result["Extension"]
	# publisher = result["Publisher"]
	# mirrors = [result["Mirror_1"], result["Mirror_2"]]

	print(f"[*]{results.index(result)}.{title}\nBy:{author}\nSize:{size}({extention}\n)")


book = results[inp_to_int(input("Select the book for download."))]

response = requests.get(book["Mirror_1"])

#BeautifulSoup gets the download link
soup = BeautifulSoup(response.content, 'html.parser') 

div = soup.find('div', id="download")
download_link = div.h2.a.get('href')

file_name = book["Title"]+"."+book["Extension"]

print("[DOWNLOADING] Requisting book, please wait.....")
urllib.request.urlretrieve(download_link, "./Downloads/"+file_name)




print(f"[DONE] {book['Title']} Saved!")