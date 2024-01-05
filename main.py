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

search_choice = input("Enter 1 to search by author,any number for search by title.")

if search_choice == 1:
	author = input("Who is the author?")
	results = s.search_author(author)
else:
	title = input("What is the book titled?")
	results = s.search_title(title)


for result in results:
	author = result["Author"]
	title = result["Title"]
	publisher = result["Publisher"]
	title = result["Title"]
	size = result["Size"]
	extention = result["Extension"]
	mirrors = [result["Mirror_1"], result["Mirror_2"]]

	print(f"[*]{results.index(result)}.{title}\nBy:{author}\nSize:{size}({extention}\n)")

book = inp_to_int(input("Select the book for download."))

book = results[book]

response = requests.get(book["Mirror_1"])
# response = requests.get("http://library.lol/main/BE9884DFAD35CF3C240B774E8810413B")

#BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser') 

div = soup.find('div', id="download")
book_link = div.h2.a.get('href')
# print(div.h2.a.get('href'))
print(book_link)

file_name = book["Title"]+"."+book["Extension"]

f = open(file_name, "w")
f.close()

print("Requisting book, please wait.....")
# book_request = requests.get(book_link)
urllib.request.urlretrieve(book_link, "Downloads/"+file_name)

# print("Book recieved, saving ....")
# # print(response)
# with open(book["Title"]+"."+book["Extension"], "wb") as f:
# 	f.write(response.content)

# print(results[0]["Mirror_1"])



print(f"{book['Title']}Saved")